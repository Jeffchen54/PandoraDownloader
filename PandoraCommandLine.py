import Services
from Services import Config

class CommandLineParser():
    """
    Parses command line for Pandora. 
    When provided with command line arguments, returns a tuple
    of dict that contains a supported service name and their
    configuration adjustments.
    """

    def parse_cmd(argv:list[str])->list[tuple]|None:
        """
        Parse CMD, should be equal to sys.argv or an equivalent.
        
        """
