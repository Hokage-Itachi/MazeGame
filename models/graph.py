class Node:
    label = ""
    adjNodes = []
    x = y = f = g = h = 0
    parent = None

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y

    def compareTo(self, node):
        if(self.f < node.f):
            return -1
        elif self.f > node.f:
            return 1
        else:
            return 0

    def equals(self, node):
        if (self.x == node.x and self.y == node.y):
            return True
        return False

    def hello():
        print("AM")


class Graph:
    nodes = []
    numEdge = 0

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def addEdge(self, v, u):
        if (v not in u.adjNodes) and (u not in v.adjNodes):
            v.adjNodes.append(u)
            u.adjNodes.append(v)
            self.numEdge += 1

    def remove(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for x in self.nodes:
                if node in x.adjNodes:
                    x.adjNodes.remove(node)
                    self.numEdge -= 1
