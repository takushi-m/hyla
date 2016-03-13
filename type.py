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
