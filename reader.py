import re

class Reader:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0

    def next(self):
        self.pos += 1
        return self.tokens[self.pos-1]

    def peek(self):
        return self.tokens[self.pos]

def read_str(line):
    tokens = tokenizer(line)
    reader = Reader(tokens)
    return read_form(reader)

def tokenizer(string):
    return re.findall(r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\"])*\"|;.*|[^\s\[\]{}('\"`,;)]*)", string)

def read_form(reader):
    tk = reader.peek()
    if tk=="(" or tk=="[":
        return read_list(reader)
    elif tk=="@":
        reader.next()
        return ["deref", read_form(reader)]
    elif tk=="'":
        reader.next()
        return ["quote", read_form(reader)]
    elif tk=="`":
        reader.next()
        return ["quasiquote", read_form(reader)]
    elif tk=="~":
        reader.next()
        return ["unquote", read_form(reader)]
    elif tk=="~@":
        reader.next()
        return ["splice-unquote", read_form(reader)]
    else:
        return read_atom(reader)

def read_list(reader):
    res = []
    reader.next()
    while reader.peek()!=")" and reader.peek()!="]":
        a = read_form(reader)
        if a!=None:
            res.append(a)
        reader.next()

    return res

def read_atom(reader):
    tk = reader.peek()
    if re.search(r"^[0-9]+$", tk)!=None:
        return int(tk)
    elif tk=="true":
        return True
    elif tk=="false":
        return False
    else:
        return tk
