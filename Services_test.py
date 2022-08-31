import logging
import unittest
import Services
from Services import Service



class ServicesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """
        No objects so no object setup needed, just turn logging switch on
        """
        logging.basicConfig(level=logging.INFO)

    def test_get_switch_to_config_table(self):
        """
        tests get_switch_to_config_table
        Info: needs to be updated given adjustments in Config
        """
        s = Services.get_switch_to_config_table()
        m = dict({'-d': (('-d', '--download_folder'), 6, Service.BASIC, "<path> : REQUIRED - Set download path for single instance, must use '\\' or '/'"), '--download_folder': (('-d', '--download_folder'), 6, Service.BASIC, "<path> : REQUIRED - Set download path for single instance, must use '\\' or '/'"), '-v': (('-v', '--verbose'), 1, Service.BASIC, ': 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all'), '--verbose': (('-v', '--verbose'), 1, Service.BASIC, ': 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all'), '-t': (('-t', '--threads'), 1, Service.BASIC, '<#> : Change download thread count (default is 6)'), '--threads': (('-t', '--threads'), 1, Service.BASIC, '<#> : Change download thread count (default is 6)'), '-c': (('-c', '--chunk_sz'), 1, Service.BASIC, '<#> : Adjust download chunk size in bytes (Default is 64M)'), '--chunk_sz': (('-c', '--chunk_sz'), 1, Service.BASIC, '<#> : Adjust download chunk size in bytes (Default is 64M)'), '-f': (('-f', '--bulk'), 5, Service.BASIC, '<textfile.txt> or <url>: Bulk download from text file containing links'), '--bulk': (('-f', '--bulk'), 5, Service.BASIC, '<textfile.txt> or <url>: Bulk download from text file containing links'), '-u': (('-u', '--unzip'), 0, Service.BASIC, ': Enables unzipping of files automatically, requires 7z and setup to be done correctly'),
                 '--unzip': (('-u', '--unzip'), 0, Service.BASIC, ': Enables unzipping of files automatically, requires 7z and setup to be done correctly'), '-z': (('-z', '--http_codes'), 4, Service.BASIC, '"500, 502,..." : HTTP codes to retry downloads on, default is 429 and 403'), '--http_codes': (('-z', '--http_codes'), 4, Service.BASIC, '"500, 502,..." : HTTP codes to retry downloads on, default is 429 and 403'), '-r': (('-r', '--http_retries'), 1, Service.BASIC, '<#> : Maximum number of HTTP code retries, default is infinite'), '--http_retries': (('-r', '--http_retries'), 1, Service.BASIC, '<#> : Maximum number of HTTP code retries, default is infinite'), '-h': (('-h',), -1, Service.BASIC, ': Help'), '--kxftype': (('--kxftype',), 2, Service.KEMONO, '<download format> : Custom file name, tokens-> [#] counter, [server] -> server name'), '--kxfile': (('--kxfile',), 3, Service.KEMONO, '"txt, zip, ..., png" : Exclude files with listed extensions, NO \'.\'s'), '--kxpost': (('--kxpost',), 3, Service.KEMONO, '"keyword1, keyword2,..." : Keyword in excluded posts, not case sensitive'), '--kxlink': (('--kxlink',), 3, Service.KEMONO, '"keyword1, keyword2,..." : Keyword in excluded link, not case sensitive. Is for link plaintext, not its target'), '--kfstructure': (('--kfstructure',), 1, Service.KEMONO, '<#> : 0 for packed, 1 for partial unpacked, 2 for unpacked')})
        self.assertEqual(s, m)

    def test_get_switch_to_info_table(self):
        """
        tests get_switch_to_info_table
        """
        s = Services.get_switch_to_info_table()
        m = dict({'-d': (0, 6, Service.BASIC), '--download_folder': (0, 6, Service.BASIC), '-v': (1, 1, Service.BASIC), '--verbose': (1, 1, Service.BASIC), '-t': (2, 1, Service.BASIC), '--threads': (2, 1, Service.BASIC), '-c': (3, 1, Service.BASIC), '--chunk_sz': (3, 1, Service.BASIC), '-f': (4, 5, Service.BASIC), '--bulk': (4, 5, Service.BASIC), '-u': (5, 0, Service.BASIC), '--unzip': (
            5, 0, Service.BASIC), '-z': (6, 4, Service.BASIC), '--http_codes': (6, 4, Service.BASIC), '-r': (7, 1, Service.BASIC), '--http_retries': (7, 1, Service.BASIC), '-h': (8, -1, Service.BASIC), '--kxftype': (9, 2, Service.KEMONO), '--kxfile': (10, 3, Service.KEMONO), '--kxpost': (11, 3, Service.KEMONO), '--kxlink': (12, 3, Service.KEMONO), '--kfstructure': (13, 1, Service.KEMONO)})
        self.assertEqual(s, m)
        
if __name__ == '__main__':
    unittest.main()
