####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) Salvaire Fabrice 2015
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

class DependencyGraphNode(object):

    ##############################################

    def __init__(self, parents=None):

        if parents is None:
            self.parents = []
        else:
            self.parents = parents
        self.childs = []

    ##############################################

    def connect_parents(self, parents):

        self.parents = list(parents)
        for node in self.parents:
            node.childs.append(self)

    ##############################################

    def top_down_visit(self):

        """ breadth first Search """

        queue = [self]
        visited = set((self,))
        while queue:
            node = queue.pop(0)
            yield node
            for child in node.childs:
                if child not in visited:
                    queue.append(child)
                    visited.add(child)

####################################################################################################

class DependencyGraph(object):

    ##############################################
    
    def __init__(self, root):

        self.root = root
        self._nodes = {root.name: root}

    ##############################################

    def __iter__(self):

        return iter(self._nodes.values())

    ##############################################

    def __getitem__(self, key):

        return self._nodes[key]

    ##############################################

    def add_node(self, node):

        node_id = node.name # hash must return an int
        if node_id not in self._nodes:
            self._nodes[node_id] = node
        else:
            raise NameError("Node {} is already registered".format(node_id))

    ##############################################

    def top_down_visit(self):

        yield from self.root.top_down_visit()

####################################################################################################
# 
# End
# 
####################################################################################################
