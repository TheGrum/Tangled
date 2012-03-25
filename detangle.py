#!/usr/bin/python

from sys import argv
import fileinput
from collections import deque
import itertools

class tree:
    def __init__(self, line):
        self.root = None
        self.name = line[5:line.find(' ',6)]
        self.parse(line[line.find('(',6)+1:].strip(';'))
        d = deque()
        self.twist_apply_list = self.root.non_leaves(d)

    def parse(self, line):
        curstr = line
        self.root = node();
        cur = self.root;
        stack = [self.root];
        while len(curstr) > 0:
            if curstr[0] == '(':
                temp = node()
                cur.add(temp)
                stack.append(cur)
                cur = temp
                curstr = curstr[1:]
            elif curstr[0] == ',':
                curstr = curstr[1:]
            elif curstr[0] == ')':
                cur = stack.pop()
                curstr = curstr[1:]
            else:
                comma = curstr.find(',')
                paren = curstr.find(')')
                if comma == -1:
                    comma = paren
                if paren == -1:
                    paren = comma
                if min(comma,paren) > -1:
                    name = curstr[0:min(comma,paren)]
                    cur.add(node(name))
                    curstr = curstr[min(comma,paren):]
                else:
                    curstr = ''

    def leaves(self):
        d = deque()
        self.root.leaves(d)
        return d

    def apply_twists(self, twists):
        for i in range(0,min(len(self.twist_apply_list),len(twists))):
            self.twist_apply_list[i].twist(twists[i])

    def print_tree(self):
        print self.name
        self.root.output(1)       
    
class node:
    def __init__(self, name=None):
        self.children = []
        self.twist = 0
        self.name = name

    def twist(self, n):
        self.twist = n

    def add(self, n):
        self.children.append(n)

    def get_children(self):
        d = deque(self.children)
        d.rotate(self.twist)
        return d

    def leaves(self, d):
        if len(self.children) == 0:
            d.append(self.name)
        else:
            c = self.get_children()
            for n in c:
                n.leaves(d)

    def non_leaves(self, d):
        if len(self.children) == 0:
            pass
        else:
            d.append(self)
            c = self.get_children()
            for n in c:
                n.leaves(d)        

    def output(self, depth):
        if len(self.children) == 0:
            print depth * ' ', '|', self.name
        else:
            d = self.get_children()
            for n in d:
                n.output(depth+1)

def tangle_count_all():
    l = [tr.leaves() for tr in trees.itervalues()]
    print l
    count = 0
    for (a,b) in itertools.combinations(l,2):
        count = count + tangle_count(a,b)
    return count
    
def tangle_count(a, b):
    count = 0
    t = dict((b[i],i) for i in range(0,len(b)))
    
    for i in range(1,min(len(a),len(b))):
        if t[a[i]] > t[a[i-1]]:
            count = count + 1
    return count
        
trees = {}

if __name__=='__main__':
    for line in fileinput.input():
        #line = line.trim()
        if line[0:4] == 'tree':
            tr = tree(line)
            trees[tr.name] = tr
            #print trees
    for tr in trees.itervalues():
        print tr
        tr.print_tree()
        pass
    print tangle_count_all()              
