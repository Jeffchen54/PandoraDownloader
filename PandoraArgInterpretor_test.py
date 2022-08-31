import unittest
import PandoraArgInterpretor
import logging
import Services

class PandoraArgInterpretorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """
        Nothing to set up except logging type
        """
        logging.basicConfig(level=logging.INFO)
    
    def test_help(self):
        """
        test lines containing help
        """
        # Only
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-h']))
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '--help']))
        
        # Beginning
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-h', '-u', 'u']))
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '--help', '-u', 'u']))
        
        # Middle
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', '-h', 'u']))
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', '--help', 'u']))
        
        # End
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', 'u', '-h']))
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', 'u', '--help']))
        
    def test_unknown_command(self):
        """
        Tests lines containing unknown commands
        """
        # Only
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '--doesnotexists']))
        # Beginning
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '--doesnotexists', '-u', '-u']))
        # Middle
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', '--doesnotexists', '-u']))
        # End
        self.assertIsNone(PandoraArgInterpretor.interpret(['.py', '-u', '-u', '--doesnotexists']))
        
    def test_independent_switches(self):
        """
        Test independent switches
        """
        
        # Only
        args = PandoraArgInterpretor.interpret(['.py', '-u'])
        self.assertTrue(args[Services.Service.BASIC][Services.Config.UNZIP.value])

        
        # Begin
        args = PandoraArgInterpretor.interpret(['.py', '-u', '-t', '64'])
        self.assertTrue(args[Services.Service.BASIC][Services.Config.UNZIP.value])
        self.assertEqual(64, args[Services.Service.BASIC][Services.Config.THREAD_COUNT.value])
        
        # Middle
        args = PandoraArgInterpretor.interpret(['.py', '-c', '6400', '-u', '-t', '64'])
        self.assertTrue(args[Services.Service.BASIC][Services.Config.UNZIP.value])
        self.assertEqual(64, args[Services.Service.BASIC][Services.Config.THREAD_COUNT.value])
        self.assertEqual(6400, args[Services.Service.BASIC][Services.Config.DOWNLOAD_CHUNK_SZ.value])
        
        # End
        args = PandoraArgInterpretor.interpret(['.py', '-t', '64', '-u'])
        self.assertTrue(args[Services.Service.BASIC][Services.Config.UNZIP.value])
        self.assertEqual(64, args[Services.Service.BASIC][Services.Config.THREAD_COUNT.value])        
        
    def test_dependent_switches(self):
        """
        Tests dependent switches
        """
        
        # Only
        args = PandoraArgInterpretor.interpret(['.py', '-t', '64'])
        self.assertEqual(64, args[Services.Service.BASIC][Services.Config.THREAD_COUNT.value])
        
        # 3
        args = PandoraArgInterpretor.interpret(['.py', '-c', '6400', '-r', '100', '-t', '64'])
        self.assertEqual(100, args[Services.Service.BASIC][Services.Config.HTTPS_RETRIES.value])
        self.assertEqual(64, args[Services.Service.BASIC][Services.Config.THREAD_COUNT.value])
        self.assertEqual(6400, args[Services.Service.BASIC][Services.Config.DOWNLOAD_CHUNK_SZ.value])    
        
        # Missing
        args = PandoraArgInterpretor.interpret(['.py', '-t'])
        self.assertIsNone(args)
    
    
    def test_list_args(self):
        """
        Tests various list switches
        """
        # Only
        
        # Begin
        
        # Middle
        
        # End
        
    def test_file_path(self):
        """
        Tests file path processing
        """
        
        # Standard windows
        
        # Nonstandard windows
        
        # ./
        
        # ../
        
        # ../somedir/something
        
    def test_folder_path(self):
        """
        Test folder path processing
        """
        # Standard windows
        
        # Nonstandard windows
        
        # ./
        
        # ../
        
        # ../somedir/
        
        # Standard window missing \\
        
        # Nonstandard windows missing /
        
        # .
        
        # ..
        
        # ../somedir

if __name__ == '__main__':
    unittest.main()