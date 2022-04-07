import unittest
import methods

class TestMethods(unittest.TestCase):

    def testAdd2(self):
        self.assertEqual(methods.add2(5), 7)


if __name__ == '__main__':
    unittest.main()
