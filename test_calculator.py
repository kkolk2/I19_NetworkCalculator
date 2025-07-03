import unittest
import conversions as mc
import functions as mf

class calculator_test(unittest.TestCase): 
    

    def test_search_raise(self):
        with self.assertRaises(ValueError):
            mf.Search("aaa aaa aa ","aa") 

    

if __name__ == '__main__': 
    unittest.main()