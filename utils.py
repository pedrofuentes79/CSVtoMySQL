keywords = []
with open("keywords.txt") as f:
    for line in f:
        keywords.append(line[:-1])

def apostrophe_remover(s, d):
    res = ""
    subvariable = ""
    reading_variable = False
    for i in range(len(s)):
        if not reading_variable:
            if s[i] != "'":
                res += "".join(s[i])
            elif s[i] == "%":
                reading_variable = True
        else:
            for j in range(len(s[i+1:])):
                if s[i+1:][j:j+1] != ")s":
                    subvariable += "".join(s[i+1:][j])
                else:
                    break
            for k in d[subvariable]:
                res += "".join(k)
    return res

def space_remover(s):
    res = ""
    for i in s:
        if i != " ":
            res += "".join(i)
        else:
            res +="".join("_")
    return res

def check_keywords(s):
    return (s + "_" if s.upper() in keywords else s)

def quote_remover(s):
    res = ""
    for i in s:
        if i != '"':
            res += "".join(i)
        else:
            res += "".join("'")
    return res