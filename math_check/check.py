import re
from .math_normalize import normalize_answer
from .grader import grade_answer

judge_math_en_version = "1"

def extract_answer(last_sentence, prompt):
    res = []

    def _trim_closed_bracket(str):
        num = 0
        idx = 0
        while idx < len(str):
            if str[idx] in ["(", "{", "["]:
                num += 1
            if str[idx] in [")", "}", "]"]:
                num -= 1
                if num == 0:
                    return str[:idx+1]
            idx += 1
        return str

    def _get_last_boxed(s):
        s = s.replace("\\boxed", "\n\n\\boxed").split("\n\n")[-1]
        s = _trim_closed_bracket(s)
        res = re.search(r"\\boxed{([\s\S]*)}", s)
        if res:
            return res.group(1)
        else:
            return None

    def _get_last_digit(s):
        _PAT_LAST_DIGIT = re.compile(r"([+-])?[0-9\.+-,]+")
        match = list(reversed(list(_PAT_LAST_DIGIT.finditer(s))))
        res = []

        for m in match:
            last_digit = m.group().replace(",", "").strip().rstrip(".")
            if last_digit == "." or not last_digit:
                continue
            res.append(last_digit)
            if last_digit not in prompt:
                break
        return res

    def _get_last_dollars(s):
        _PAT_LAST_DOLLARS = re.compile(r"\$(.+?)\$")
        match = list(reversed(list(_PAT_LAST_DOLLARS.finditer(s))))
        res = []

        for m in match:
            last_digit = m.group().strip()
            res.append(last_digit)
            if last_digit not in prompt:
                break
        return res

    exit_flag = False
    x = _get_last_boxed(last_sentence)
    if x:
        res.append(x)
        return res, True

    if re.search(r"(=|\b(is|to)\b)", last_sentence):
        res.append(re.split(r"(=|\b(is|to)\b)", last_sentence)[-1].split("$")[0].strip().rstrip("."))
    x = _get_last_dollars(last_sentence)
    if x:
        exit_flag = True
        res.extend(x)
    x = _get_last_digit(last_sentence)
    if x:
        exit_flag = True
        res.extend(x)
    if len(last_sentence) <= 20 and any([t in last_sentence for t in "$\\{}0123456789"]):
        res.append(last_sentence)
    # if not res:
    #     res.append(re.split(r"[\s]", last_sentence)[-1])

    return [x for x in res if x], exit_flag

def check_correctness_math(entry, gen, max_extract_answer_trials=3, max_string_match_trails=1):

    assert max_string_match_trails <= max_extract_answer_trials

    answer = str(entry['answer_only'])
    prompt = entry['question']
    last_sentence = None
    trial = 0
    exit = False
    extracted_answer = []

    for s in reversed(re.split(r"((?<=[^.]{3})\.(?=[^0-9])(?=[^.]{3}))|(\\end{align\*})|(?<=[\.|^])\\]|(\n)", gen)):
        s = s.strip() if s else ""
        s = s.replace("\\end{align*}", "").rstrip(".")
        last_sentence = s
        if not s or (s == "\\]" or s == "]" or s == "." or s == "$" or s == "$$" or s == "[/asy]" or s == "}"):
            continue

        trial += 1
        preds, exit = extract_answer(last_sentence, prompt)  # try to extract answer
        if preds:
            for pred in preds:
                extracted_answer.append(pred)
                if grade_answer(pred, answer):
                    #return {'accuracy': 1.0, "extracted_answer": extracted_answer}
                    return True

        if trial <= max_string_match_trails:
            # fallback to match string
            answers = [answer.rstrip("."), normalize_answer(answer)]
            flag = False
            for try_ans in answers:
                if re.match(r"^-?[\d\.]+$", try_ans) is None:
                    if not flag:
                        extracted_answer.append(last_sentence)
                        flag = True

                    if try_ans.startswith("/") and try_ans.endswith("/"): # regex
                        pattern = try_ans[1:-1]
                    else:
                        pattern = r"(?:^|[^0-9])" + re.escape(try_ans) + r"(?:[^0-9]|$)"
                    if re.search(pattern, last_sentence) is not None:
                        #return {'accuracy': 1.0, "extracted_answer": extracted_answer}
                        return True
        
        if trial >= max_extract_answer_trials or exit:
            break
    #return {'accuracy': 0.0, "extracted_answer": extracted_answer}
    return False
