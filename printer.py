import types
from type import Atom

def pr_str(mal_data, print_readably=True):
    res = []
    if isinstance(mal_data, (types.LambdaType,dict)):
        return "#<function>"
    elif isinstance(mal_data,bool):
        if mal_data:
            return "true"
        else:
            return "false"
    elif isinstance(mal_data,str):
        if print_readably:
            mal_data = mal_data.replace("\\n","\n").replace("\\\"","\"").replace("\\\\","\\")
        return mal_data
    elif isinstance(mal_data,Atom):
        return "(atom "+str(mal_data.value)+")"
    elif not isinstance(mal_data, list):
        return str(mal_data)

    for tk in mal_data:
        if isinstance(tk,list):
            res.append(pr_str(tk))
        else:
            res.append(pr_str(tk))
    return "("+" ".join(res)+")"
