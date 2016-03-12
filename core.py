import printer
import reader
import re
from type import Atom

def malstring2pythonstring(s):
    a = re.search(r"\"((?:\\.|[^\"])*)\"", s)
    return a.group(1)

def readfile(name):
    name = malstring2pythonstring(name)
    ret = "";
    with open(name,"r") as f:
        ret = f.read()
    return ret.replace("\"","\\\"")

def concat(*lst):
    ret = []
    for l in lst:
      ret.extend(l)
    return ret

def nth(lst,idx):
    if idx<0 or idx>=len(lst):
        raise "out of range"
    else:
        return lst[idx]

def rest(lst):
    if lst=="nil":
        return []
    elif len(lst)<2:
        return []
    else:
        return lst[1:len(lst)]

def throw(s):
    raise Exception(s)

def prn(*x):
    print(" ".join([printer.pr_str(v,True) for v in x]))
    return "nil"

def apply(f,*lst):
    arg = []
    for l in lst:
        if isinstance(l,list):
            arg.extend(l)
        else:
            arg.append(l)
    if isinstance(f,dict):
        return f["fn"](*arg)
    else:
        return f(*arg)

ns = {
    "+": lambda x,y: x+y
    ,"-": lambda x,y: x-y
    ,"*": lambda x,y: x*y
    ,"/": lambda x,y: x/y
    ,"nil": "nil"
    ,"not": lambda x: not ((type(x)==bool and x) or (type(x)!=bool and x!="nil"))
    ,"list": lambda *l: [*l]
    ,"list?": lambda lst: isinstance(lst,list)
    ,"empty?": lambda lst: len(lst)==0
    ,"count": lambda lst: len(lst) if isinstance(lst,(list,tuple)) else 0
    ,"=": lambda x,y: x==y
    ,">": lambda x,y: x>y
    ,"<": lambda x,y: x<y
    ,">=": lambda x,y: x>=y
    ,"<=": lambda x,y: x<=y
    ,"read-string": lambda s: reader.read_str(malstring2pythonstring(s))
    ,"slurp": lambda fname:"\""+readfile(fname)+"\""
    ,"str": lambda *x: "\""+"".join([malstring2pythonstring(printer.pr_str(v,False)) for v in x])+"\""
    ,"prn": prn
    ,"atom": lambda v:Atom(v)
    ,"atom?": lambda a:isinstance(a,Atom)
    ,"deref": lambda a:a.value
    ,"reset!": lambda a,v:a.reset(v)
    ,"swap!": lambda a,f,*arg:a.reset(f(a.value,*arg) if not isinstance(f,dict) else f["fn"](a.value,*arg))
    ,"cons": lambda a,lst: [a,*lst]
    ,"concat": concat
    ,"nth": nth
    ,"first": lambda lst:"nil" if len(lst)==0 or lst=="nil" else nth(lst,0)
    ,"rest": rest
    ,"throw": throw
    ,"apply": apply
    ,"map": lambda f,lst: [f(x) for x in lst] if not isinstance(f,dict) else [f["fn"](x) for x in lst]
    ,"nil?": lambda s:s=="nil"
    ,"true?": lambda b:isinstance(b,bool) and b
    ,"false?": lambda b:isinstance(b,bool) and not b
    ,"symbol?": lambda s:isinstance(s,str) and s!="nil" and re.search("^[^\s\[\]{}('\"`,;)]*$",s)!=None
    ,"symbol": malstring2pythonstring
}
