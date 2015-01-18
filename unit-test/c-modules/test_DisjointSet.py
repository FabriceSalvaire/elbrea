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

        for i in xrange(disjoint_set_size):
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
