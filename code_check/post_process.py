import re


def remove_after_return(code):
    """
    Takes as input a code, and removes everything that is after the return.
    That is, the first line that does not start with a space character
    """
    pattern = r"[^\n]+(\n|$)"
    end_last_match = None
    # Go trough the regex to match any sequence of characters ending with a \n
    for match in re.finditer(pattern, code):
        start_match, end_match = match.span()
        # Search for the first line which does not start by a space character
        if (
            end_last_match is not None
            and start_match < len(code)
            and code[start_match].strip() != ""
        ):
            return code[0: start_match]
        end_last_match = end_match
    return code


def process_text(text,entry_point):

    text = text.strip('\n')
    #if not text.startswith('    '):
    x = re.search(r"```python(.+?)```",text,flags=re.DOTALL)
    if x!=None:
        if f'def {entry_point}' in text[x.span()[0]+9:x.span()[1]-3]:
            text = text[x.span()[0]+9:x.span()[1]-3]
    x = re.search(r"```(.+?)```",text,flags=re.DOTALL)
    if x!=None:
        if f'def {entry_point}' in text[x.span()[0]+3:x.span()[1]-3]:
            text = text[x.span()[0]+3:x.span()[1]-3]
    x = re.search(r"```python(.+)",text,flags=re.DOTALL)
    if x!=None:
        text = text[x.span()[0]+9:x.span()[1]]
    x = re.search(r"(.+)```",text,flags=re.DOTALL)
    if x!=None:
        text = text[x.span()[0]:x.span()[1]-3]

    #try:
    text = text.strip()
    x = re.search(rf"def {entry_point}[^\n]+(\n|$)",text) 
    
    if x!=None:
        start,end = x.span()

        prefix = text[:start]
        text = text[end:]
        if len(prefix.split('\n'))!=0:
            l = prefix.split('\n')
            l = [line.strip() for line in l]
            for idx,line in enumerate(l):
                
                if line.startswith("def") or line.startswith("from ") or line.startswith("import"):
                    prefix = "\n    "+"\n    ".join(l[idx:])+'\n'
                    break
                else:
                    prefix=''

            text = prefix + text 

    text = remove_after_return(text)
    return text