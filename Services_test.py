import logging
import unittest
import Services

class ServicesTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        """
        No objects so no object setup needed, just turn logging switch on
        """
        logging.basicConfig(level=logging.INFO)
        
    def test_help(self):
        """
        Tests help
        """
        Services.print_help()

if __name__ == '__main__':
    unittest.main()
