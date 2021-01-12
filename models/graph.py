class Node:

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y
        self.g = 0 # Distance to start node
        self.h = 0 # Distace to goal node
        self.f = 0 # Total cost
        self.adjNodes = []
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        # print(other.__repr__())
        if (self.x == other.x and self.y == other.y):
            return True
        return False

     # Print node
    def __repr__(self):
        return ('({0}: x = {1}, y = {2})'.format(self.label, self.x, self.y))

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

    def remove_edge(self, u, v):
        if (v in u.adjNodes) and (u in v.adjNodes):
            v.adjNodes.remove(u)
            u.adjNodes.remove(v)
            self.numEdge -= 1
    def get_node_from_position(self, position):
        for node in self.nodes:
            if(node.x == position[0] and node.y == position[1]):
                return node
        return Node("", position[0], position[1])