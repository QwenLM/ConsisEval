<div align="center">
  <h2><i>ConsisEval:</i> A Hard-to-Easy Consistency Evaluation<br>Benchmark for Large Language Models</h2> 
</div>



<!-- This is the repo for our paper: Can Large Language Models Always Solve Easy Problems if They Can Solve Harder Ones? -->

- This repo is for paper [Can Large Language Models Always Solve Easy Problems if They Can Solve Harder Ones?](https://arxiv.org/abs/2406.12809)
- Our code and data will be released soon!

## Overview

ConsisEval is developed to systematically evaluate the hard-to-easy consistency of LLMs. Here the hard-to-easy inconsistency refers to the counter-intuitive phenomenons where LLMs, while capable of solving hard problems, can paradoxically fail at easier ones.  

ConsisEval includes 732 pair of questions from code (164), mathematics (298), and instruction-following (270) domains. It is noteworthy that there are only pairwise data in ConsisEval: one datum is comprised of two questions (an easy question and a harder one), and there is a strict order of difficulty between these two questions.

## Data Collection

- Easy data is collected from [gsm8k](https://github.com/openai/grade-school-math), [IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) and [HumanEval](https://github.com/openai/human-eval).
- hard data derived from easy data by automatic generation and human annotation.

## Evaluation Metric

- Consistency Score (CS): conditional probability of a model correctly answering easy questions provided that it has correctly answered harder ones. 


## Code and Data

- Our code and data will be released soon!

## Citation

<!-- If you find the resources in this repository useful, please cite our paper: -->

```
@misc{yang2024large,
      title={Can Large Language Models Always Solve Easy Problems if They Can Solve Harder Ones?}, 
      author={Zhe Yang and Yichang Zhang and Tianyu Liu and Jian Yang and Junyang Lin and Chang Zhou and Zhifang Sui},
      year={2024},
      eprint={2406.12809},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
