import json
import argparse
import math


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name',type=str)
    parser.add_argument('--task',type=str)
    args = parser.parse_args()
    assert args.task in ['code','math','instruction_following'], 'Only \'code\', \'math\', \'instruction_following\' are supported for args.task'
    model_name = args.model_name.split("/")[-1]

    hard_dic, easy_dic = {}, {}
    with open(f"log/{model_name}_{args.task}_hard.jsonl") as f:
        for line in f.readlines():
            tmp = json.loads(line)
            key = tmp["key"]
            if key not in hard_dic.keys():
                hard_dic[key] = []
            hard_dic[key].append(tmp['passed'])

            
    with open(f"log/{model_name}_{args.task}_easy.jsonl") as f:
        for line in f.readlines():
            tmp = json.loads(line)
            key = tmp["key"]
            if key not in easy_dic.keys():
                easy_dic[key] = []
            easy_dic[key].append(tmp['passed'])
    
    
    if args.task == 'math':
        assert len(easy_dic) == 298 and len(hard_dic) == 298 
    elif args.task == 'code':
        assert len(easy_dic) == 164 and len(hard_dic) == 164
    elif args.task == 'instruction_following':
        assert len(easy_dic) == 270 and len(hard_dic) == 270

    P_easy_list = [sum(l)/len(l) for l in easy_dic.values()]
    P_hard_list = [sum(l)/len(l) for l in hard_dic.values()]

        
    P_easy_and_hard_list = [e*h for e,h in zip(P_easy_list,P_hard_list)]
    P_easy = sum(P_easy_list)/len(P_easy_list)
    P_hard = sum(P_hard_list)/len(P_hard_list)
    P_easy_and_hard = sum(P_easy_and_hard_list)/len(P_easy_and_hard_list)
    P_easy_given_hard = P_easy_and_hard/P_hard

    upper_bound_sort = sum([e*h for e,h in zip(sorted(P_easy_list),sorted(P_hard_list))])/len(P_easy_list)/P_hard 
    lower_bound_sort = sum([e*h for e,h in zip(sorted(P_easy_list),sorted(P_hard_list,reverse=True))])/len(P_easy_list)/P_hard 
    
    lower_bound = P_easy 

    upper_bound1 = sum([e*max(e-P_easy+P_hard,0) for e in P_easy_list])/len(P_easy_list)/P_hard # 期望上界
    upper_bound = sum([h*(min(h+P_easy-P_hard,1)) for h in P_hard_list])/len(P_easy_list)/P_hard # 期望上界\
    
    print(args.model_name)
    print(f"Hard Acc = P(hard) = {100*P_hard} %")
    print(f"Easy Acc = P(easy) = {100*P_easy} %")
    print(f"CS = P(easy|hard) = {100*P_easy_given_hard} %")

    final_bound = 1
    for bound in [upper_bound,upper_bound1,upper_bound_sort]:
        if bound>P_easy_given_hard and bound<final_bound:
            final_bound = bound
    print()
    print(f"Lower bound = {100*lower_bound} %")
    print(f"final_upper_bound: {100*final_bound} %")
    print(f"RCS = {100*(P_easy_given_hard - lower_bound)/(final_bound-lower_bound)} %")

    print('*'*50)



if __name__ == '__main__':
    main()

        