TOKENIZERS_PARALLELISM=true \
python eval.py \
 --model_name meta-llama/Meta-Llama-3-8B-Instruct \
 --model_path /path/to/your/model/ \
 --task math \
 --device cuda:0 \
 --debug \
 --force
