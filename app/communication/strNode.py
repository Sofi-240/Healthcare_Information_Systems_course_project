class node:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def hasChild(self, name):
        if not self.children.get(name):
            return False
        return True

    def append(self, child):
        if not self.children.get(child.name):
            self.children[child.name] = child
            return child
        return self.children.get(child.name)

    def getChild(self, name):
        return self.children.get(name)


