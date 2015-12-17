def is_sub_query(s):
    return bool(get_outer_brackets(s))

def is_opening_bracket(s):
    return s in '(['

def is_closing_bracket(s):
    return s in ')]'

def get_outer_brackets(s):
    s = strip_suffix(s)
    if s[0] == '[' and s[-1] == ']': return '[]'
    elif s[0] == '(' and s[-1] == ')': return '()'
    return None

def get_suffix(s):
    suffix = ''
    for c in s[::-1]:
        if c in '+*?':
            suffix += c
        else:
            break
    if suffix:
        s = s[:-len(suffix)]
        has_brackets = ((len(s) >= 2) and
                (s[0] == '[' and s[-1] == ']') or (s[0] == '(' and s[-1] == ')'))        
        if has_brackets:
            return suffix[::-1]
    return ''

def strip(s):
    suffix = get_suffix(s)
    brackets = get_outer_brackets(s)
    if suffix and brackets:
        s = strip_suffix(s)
    if brackets:
        s = strip_outer_brackets(s)
    return s

def strip_outer_brackets(s):
    if get_outer_brackets(s) and len(s) >= 2:
        return s[1:-1]
    return s

def strip_suffix(s):
    suffix = get_suffix(s)
    if len(suffix):
        return s[:-len(suffix)]
    return s

