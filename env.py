class Env:
    def __init__(self,outer=None,binds=[],exprs=[]):
        self.outer = outer
        self.data = {}

        for idx,val in enumerate(binds):
            if val!="&":
                self.data[val] = exprs[idx]
            else:
                self.data[binds[idx+1]] = exprs[idx:]
                break

    def set(self,key,val):
        self.data[key] = val

    def find(self,key):
        if not isinstance(key,str):
            return None
        if key in self.data:
            return self
        elif key not in self.data and self.outer!=None:
            return self.outer.find(key)
        else:
            return None

    def get(self,key):
        env = self.find(key)
        if env == None:
            raise "not find: "+str(key)
        else:
            return env.data[key]
