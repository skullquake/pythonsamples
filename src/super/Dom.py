class Node():
    def __init__(self,n="",c=""):
        """
        ctor
        """
        self.nodename=n
        self.contents=c
        self.children=[]
        self.parent=None
        pass
    def addChild(self,o):
        """
        see name
        """
        self.children.append(o)
        return o
    def getChildren(self):
        """
        see name
        """
        return self.children
    def getDescendents(self):
        """
        see name
        """
        ret=[]
        for a in self.children:
            ret.append(a)
            for b in a.getChildren():
                ret.append(b)
        return ret
    def __str__(self,idt=0):
        """
        see name [see recursive generator like flatten]
             also do type checking, children are supposed to be widgets
        """
        ret=""
        for b in range(0,idt):
            ret+="\t"
        ret+=f"<{self.nodename}>\n"
        for a in self.getChildren():
            ret+=a.__str__(idt+1)
        for b in range(0,idt):
            ret+="\t"
        ret+=f"</{self.nodename}>\n"
        return ret
class Div(Node):
    def __init__(self):
        """
        ctor
        """
        #Node.__init__(self)
        super().__init__("div")
        pass
class Btn(Node):
    def __init__(self):
        """
        ctor
        """
        #Node.__init__(self)
        super().__init__("btn")
    def click(self):
        """
        click
        """
        #Node.__init__(self)
        super().__init__("btn")

        pass

