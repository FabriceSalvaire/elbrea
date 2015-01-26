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

# input versus parent
# output versus child

####################################################################################################

class DirectedAcyclicGraphNode(object):

    ##############################################

    def __init__(self):

        self.inputs = dict()
        self.outputs = set()

    ##############################################

    def node_id(self):
        raise NotImplementedError

    ##############################################

    def disconnect_input(self, name):

        if name in self.inputs:
            node = self.inputs[name]
            del self.inputs[name]
            node.outputs.remove(self)

    ##############################################

    def connect_input(self, name, node):

        self.disconnect_input(name)
        self.inputs[name] = node
        node.outputs.add(self)

    ##############################################

    def top_down_visit(self):

        """ breadth first Search """

        queue = [self]
        visited = set((self,))
        while queue:
            node = queue.pop(0)
            yield node
            for output in node.outputs:
                if output not in visited:
                    queue.append(output)
                    visited.add(output)

####################################################################################################

class DirectedAcyclicGraph(object):

    ##############################################
    
    def __init__(self, root):

        self.root = root
        self._nodes = {root.name: root}

    ##############################################

    def __iter__(self):

        return iter(self._nodes.values())

    ##############################################

    def __getitem__(self, node_id):

        return self._nodes[node_id]

    ##############################################

    def add_node(self, node):

        node_id = node.node_id
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
