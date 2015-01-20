####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
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

import unittest

####################################################################################################

from Elbrea.C.DisjointSet import DisjointSet
            
####################################################################################################

class TestDisjointSet(unittest.TestCase):

    ##############################################

    def __init__(self, method_name):

        super(TestDisjointSet, self).__init__(method_name)

    ##############################################
        
    def test(self):

        disjoint_set_size = 10
        compression_path = True
        disjoint_set = DisjointSet(disjoint_set_size, compression_path)

        for i in range(disjoint_set_size):
            self.assertEqual(disjoint_set.find(i), i)

        # 1 + 2 : root[1] = 2 rank[2] = 2
        self.assertEqual(disjoint_set.merge(1, 2), 2)
        # 5 + 6 : root[5] = 6 rank[6] = 2
        self.assertEqual(disjoint_set.merge(5, 6), 6)
        # 5 + 7 : root[7] = 6
        self.assertEqual(disjoint_set.merge(5, 7), 6)
        # self +
        self.assertEqual(disjoint_set.merge(7, 7), 6)
        # 7 + 1 : root[7] = root[6] = 2 rank[2] = 3
        self.assertEqual(disjoint_set.merge(7, 1), 2)
        # 1 + 3 : root[3] = 2
        self.assertEqual(disjoint_set.merge(1, 3), 2)

        # for i in xrange(disjoint_set_size):
        #     print 'Node', i, disjoint_set.find(i)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
