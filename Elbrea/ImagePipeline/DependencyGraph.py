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

    #! node_id -> name 
    #! remove data

    ##############################################

    def __init__(self, node_id, parents=None, childs=None, data=None):

        self.node_id = node_id
        if parents is None:
            self.parents = []
        else:
            self.parents = parents
        if childs is None:
            self.childs = []
        else:
            self.childs = childs
        self.data = data

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
        self.nodes = {root.node_id: root}

    ##############################################

    def add_node(self, node):

        node_id = node.node_id
        if node_id not in self.nodes:
            self.nodes[node_id] = node
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
