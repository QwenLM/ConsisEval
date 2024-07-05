from transformers import AutoTokenizer,AutoModelForCausalLM
from tqdm import tqdm
import json
import torch
import argparse
import os

from instruction_following_check.check import check_correctness_instruction_following
from math_check.check import check_correctness_math
from code_check.check import check_correctness_code
from code_check.post_process import process_text

def get_examples(task,split):
    test_examples = []
    with open(f'./data/{task}_{split}.jsonl') as f:
        for line in f.readlines():
            test_examples.append(json.loads(line))
    return test_examples

def generate_answer(model, tokenizer, question, sampling_times):

    results = []
    prompt = f'{question}'

    messages = [
        {"role": "user", "content": prompt}
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    toks = tokenizer([prompt], padding=False, return_tensors="pt").to(model.device)
    orig_len = toks["input_ids"].shape[1]

    for _ in range(sampling_times):
        with torch.no_grad():
            out = model.generate(
                **toks, max_new_tokens=1500, do_sample=True
            )
        text = tokenizer.decode(out[0,orig_len:],skip_special_tokens=True)
        results.append(text)
    return results



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--task", type=str)
    parser.add_argument("--model_path", type=str, default='')
    parser.add_argument("--sampling_times", type=int, default=20)
    parser.add_argument("--device", type=str, default='auto')
    parser.add_argument("--debug",action='store_true')
    parser.add_argument("--force",action='store_true')
    args = parser.parse_args()
    model_name = args.model_name.split("/")[-1]
    model_path = args.model_path if args.model_path!='' else args.model_name

    assert args.task in ['code','math','instruction_following'], 'Only \'code\', \'math\', \'instruction_following\' are supported for args.task'
    
    check_correctness = eval(f'check_correctness_{args.task}')

    if args.device!='auto':
        model = AutoModelForCausalLM.from_pretrained(model_path,torch_dtype=torch.float16,trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
        device = torch.device(args.device)
        model.to(device)
    else:
        model = AutoModelForCausalLM.from_pretrained(model_path,torch_dtype=torch.float16,device_map='auto',trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)

    print("Model Loaded")

    for split in ['easy','hard']:
        test_examples = get_examples(args.task, split)
        if args.debug:
            test_examples = test_examples[:5]

        output_path = f"./log/{model_name.replace('.','_')}_{args.task}_{split}{'_debug' if args.debug else ''}.jsonl"
        if not os.path.exists(output_path):
            f = open(output_path,'w')
            f.close()

        if args.force:
            write_mode = 'w'
        else:
            write_mode = 'a'
            processed_keys = set()
            with open(output_path, 'r', encoding='utf-8') as reader:
                for line in reader:
                    data = json.loads(line)
                    processed_keys.add(data['key'])
            test_examples = [d for d in test_examples if d['key'] not in processed_keys]

        with open(output_path, write_mode, encoding='utf-8') as writer:
            for test_example in tqdm(test_examples,desc=f'{args.task} {split}'):
                if args.debug:
                    sampling_times=1
                else:
                    sampling_times=args.sampling_times

                texts = generate_answer(model, tokenizer, test_example['question'], sampling_times)

                for text in texts:
                    if args.task == 'code':
                        text = process_text(text,test_example['entry_point'])
                    passed = check_correctness(test_example,text)
                    tmp = {'key':test_example['key'],'question':test_example['question'],"response":text,'passed':passed}
                    writer.write(json.dumps(tmp) + '\n')
        
        

if __name__ == "__main__":
    main()
