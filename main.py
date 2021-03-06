import re
import sys
import readline
from more_itertools import chunked

import reader
import printer
import core
from env import Env

DEBUG = False
def log(msg,label="",debug=False):
    if debug or DEBUG:
        print("["+label+"] "+msg)

def is_pair(lst):
    return isinstance(lst,list) and len(lst)>0

def quasiquote(ast):
    if not is_pair(ast):
        return ["quote",ast]
    elif ast[0] == "unquote":
        return ast[1]
    elif is_pair(ast[0]) and ast[0][0]=="splice-unquote":
        return ["concat",ast[0][1],quasiquote(ast[1:])]
    else:
        return ["cons",quasiquote(ast[0]),quasiquote(ast[1:])]

def is_macro_call(ast,env):
    if is_pair(ast) and env.find(ast[0]):
        f = env.get(ast[0])
        if isinstance(f,dict):
            return f["is_macro"]
    return False

def macroexpand(ast,env):
    while is_macro_call(ast,env):
        mac = env.get(ast[0])
        ast = mac["fn"](*ast[1:])
    return ast

def eval_ast(ast,env):
    if isinstance(ast,str):
        if re.search(r"\"(?:\\.|[^\"])*\"", ast)!=None:
            return ast
        else:
            if env.find(ast)!=None:
                return env.get(ast)
            else:
                raise Exception("\"\'"+str(ast)+"\' not found\"")
    elif isinstance(ast,list):
        return [EVAL(x,env) for x in ast]
    else:
        return ast

def READ(line):
    res = reader.read_str(line)
    log(str(res),"READ")
    return res

def EVAL(ast, env):
    if ast=="":
        return ""
    while True:
        log(str(ast),"EVAL")

        ast = macroexpand(ast,env)
        if not isinstance(ast,list):
            return eval_ast(ast,env)
        f = ast[0]
        if f=="def!":
            v = EVAL(ast[2],env)
            env.set(ast[1], v)
            return v
        elif f=="let*":
            bindings = ast[1]
            log(str(bindings),"bindings")
            if len(bindings)%2!=0:
                raise

            cenv = Env()
            cenv.outer = env
            for k,vast in chunked(bindings,2):
                v = EVAL(vast,cenv)
                cenv.set(k,v)
                new_env = Env(cenv)
                cenv = new_env

            ast = ast[2]
            env = cenv
            #return EVAL(ast[2],cenv)
        elif f=="do":
            eval_ast(ast[1:-1],env)
            ast = ast[-1]
        elif f=="if":
            cond = EVAL(ast[1],env)
            if (type(cond)==bool and cond) or (type(cond)!=bool and cond!="nil"):
                ast = ast[2]
            elif len(ast)==3:
                ast = "nil"
            else:
                ast = ast[3]
        elif f=="fn*":
            # (fn* (x y) (+ x y))
            binds = ast[1]
            body = ast[2]

            log(str(binds),"function.binds")
            log(str(body),"function.body")

            fn = lambda *param:EVAL(body,Env(env,binds,param))
            return {
                "ast": body
                ,"params": binds
                ,"env": env
                ,"fn": fn
                ,"__fn__": True
                ,"is_macro": False
            }
        elif f=="quote":
            return ast[1]
        elif f=="quasiquote":
            ast = quasiquote(ast[1])
        elif f=="defmacro!":
            fun = EVAL(ast[2],env)
            fun["is_macro"] = True
            env.set(ast[1], fun)
            return fun
        elif f=="macroexpand":
            return macroexpand(ast[1],env)
        elif f=="try*":
            # (try* A (catch* B C))
            try:
                return EVAL(ast[1],env)
            except Exception as e:
                bind = [ast[2][1]]
                expr = [e.args[0]]
                env = Env(outer=env,binds=bind,exprs=expr)
                ast = ast[2][2]
        else:
            evaled = eval_ast(ast, env)
            f = evaled[0]
            p = evaled[1:]
            if type(f)==dict:
                ast = f["ast"]
                env = Env(f["env"],f["params"],p)
            else:
                return f(*p)


def PRINT(line):
    res = printer.pr_str(line)
    log(str(res),"PRINT")
    return res

def rep(line):
    ast = READ(line)
    y = EVAL(ast,repl_env)
    z = PRINT(y)
    return z


if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=="-v":
        DEBUG = True

    repl_env = Env()
    for k,v in core.ns.items():
        repl_env.set(k,v)
    repl_env.set("eval", lambda ast:EVAL(ast, repl_env))

    rep("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \")\")))))")
    rep("(load-file \"core.hyla\")")

    while True:
        try:
            line = input("user> ")
            output = rep(line)
            print(output)
        except EOFError as e:
            break
        except Exception as e:
            print(e)
