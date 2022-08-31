import logging
import os
from Services import Service, print_help
import Services
"""
Useful interpretor which can interpret certain arguments
(if they have been implemented in Services.Config correctly)
as well as parse and prepare common data such as folder
path and file path.

Author: Jeff Chen
Date: 8/30/2022
"""

def __help_msg(error_msg:str)->None:
    """
    Outputs an error msg followed by a help message

    Args:
        arg (str): arg responsible for the error message
    """
    logging.critical("{arg}".format(arg=error_msg))
    print_help()

def interpret(args:list[str])->dict[Service.value, dict]:
    """
    Processes command line arguments and sends 
    back instructions in dict form that can be understood
    by PandoraDownloader.

    Args:
        args result from returning sys.argv or equivalent: 
    Post: any arg data that requires verfication such as a folder path 
        must be checked before use as this function only prepares 
        data, not verify it.
    Return: dict of the form {"service1":dict, "service2":dict...}
        service are member values of Services and dict is 
        {Config.value:param, Config.value:param,...}. 
        
        Config.values: associated with Config.values in Services.py
        param: param required to modify the Config.value
        
        If an unknown command is provided, None will be returned and help is printed out
        If an invalid argument is sent, None is returned.
    """
    
    # generate lookup list of configs
    config_table = Services.get_config_table()
    dict_list = dict()
    pointer = 1
    # Process each line, place it into a task list
    while(len(args) > pointer):
        # Check if arg is a valid config, if not, print help and return
        if args[pointer] not in config_table:
            
            Services.print_help("{arg} is not a valid config, please review the switches!".format(arg=args[pointer]))
            return None
        
        # Get config from table
        config = config_table[args[pointer]]
                
        # Check if service is in the dict_list, if not add an entry for it
        if config[2] not in dict_list:
            dict_list[config[2]] = dict()
        
        # Add arg to the dict_list based on config arg type
        match config[1]:
            # Help
            case -1:
                print_help()
                return None
            # bool
            case 0:
                dict_list[config[2]][config] = True
                pointer += 1
                break
            case _:
            # From this point on, next arg is needed
                if len(args) ==  pointer + 1:
                    __help_msg("{arg} does not have enough arguments -> here are the required arguments: {supplement}".format(arg=args[pointer], supplement=config[3]))
            
                match config[1]:
                    # int
                    case 1:
                        dict_list[config[2]][config] = int(args[pointer + 1])
                        break
                    # str
                    case 2:
                        dict_list[config[2]][config] = (args[pointer + 1])
                        break
                    # list[str], comma separated, to lower case
                    case 3:
                        dict_list[config[2]][config] = [token.strip().lower() for token in args[pointer + 1].split(',')]
                        break
                    # list[int], comma separated
                    case 4:
                        dict_list[config[2]][config] = [int(token.strip()) for token in args[pointer + 1].split(',')]
                        break
                    # str, absolute file path
                    case 5:
                        dict_list[config[2]][config] = process_file_path(args[pointer + 1])
                        break
                    # str, absolute dir path
                    case 6:
                        dict_list[config[2]][config] = process_dir_path(args[pointer + 1])
                        break
                pointer += 2
                    
            
            
def process_file_path(fpath:str)->str:
    """
    Prepares a file path to be processable by python

    Args:
        fpath (str): unprocessed file path

    Returns:
        str: processed and ready to use file path
    """
    return os.path.abspath(fpath)

def process_dir_path(dirpath:str)->str:
    """
    Prepares a directory path to be processable by python

    Args:
        dirpath (str): unprocessed directory path

    Returns:
        str: processed and ready to use directory path
    """
    folder = os.path.abspath(dirpath)

    if folder[len(folder) - 1] == '\"':
        folder = folder[:len(folder) - 1] + '\\'
    elif not folder[len(folder) - 1] == '\\':
        folder += '\\'
    return folder
