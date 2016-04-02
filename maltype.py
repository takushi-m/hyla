class Atom:
    def __init__(self,val):
        self.value = val

    def reset(self,val):
        self.value = val
        return val

    def tostring(self):
        return "(atom "+str(self.value)+")"

def atomp(v):
    return isinstance(v,Atom)


class String:
    def __init__(self,val):
        self.value = val.replace("\\\"","\"").replace("\\n","\n").replace("\\\\","\\")

    def tostring(self,print_readably=True):
        val = self.value
        if print_readably:
            val = val.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n")
        return val

def stringp(v):
    return isinstance(v,String)
