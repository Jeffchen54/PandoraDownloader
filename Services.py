from enum import Enum
import logging

class Services(Enum):
    """
    Services supported by PandoraDownloader
    Each member value is associated with its class instance name
    For example, Services.Kemono = KemonoComponent.
    Author: Jeff Chen
    Date: 8/29/2023
    # TODO add component
    """
    BASIC = None
    KEMONO = None

class Config(Enum):
    """
    Configurations and settings supported by Pandora. Each member value
    is associated with an integer which describes which value should be
    passed in to manipulate a configuration and the switch association
    with the config and class associated with the config
    and a description of the config.
    
    Member value format example:
    Config.A_CONFIG = (("--SWITCH USED", "-s"), 1, Services.BASIC, "Does this")
    
    Format dissection:
    Tuple[Tuple[str], int, Services.value, str]
    
    Outer tuple always size 2, inner tuple always at least size 1
    
    Integer value for a config:
    -1: help
    0: bool
    1: int, need to process next token
    2: str, need to process next token
    3: list[str], need to process next token
    4: list[int], need to process next token

    When adding configs, a specific convention must be followed.
    (1) only basic configs will have a single '-' switch
    (2) both basic and special configs use '--' switches
    (3) special config switches must start with an identifier of the service
    (4) basic config names have no prefix while special config names are prefixed with their service

    Author: Jeff Chen
    Date: 8/29/2023
    """
    # For each config, an example is provided to the right of the config
    # BASIC CONFIGS ##################################################################################
    DOWNLOAD_FOLDER = (('-d', '--download_folder'), 2, Services.BASIC,"<path> : REQUIRED - Set download path for single instance, must use '\\' or '/'")                      #'./' or '../' or '../folder/file.txt' or 'C:/user/folder' 
    VERBOSE = (('-v', '--verbose'), 1, Services.BASIC, ": 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all")                                 # 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all
    THREAD_COUNT = (('-t', '--threads'), 1, Services.BASIC, "<#> : Change download thread count (default is 6)")                                                                # 6 for six threads
    DOWNLOAD_CHUNK_SZ = (('-c', '--chunk_sz'), 1, Services.BASIC, "<#> : Adjust download chunk size in bytes (Default is 64M)")                                                 # 6400000 for ~64MBs
    DOWNLOAD_URL = (('-f', '--bulk'), 2, Services.BASIC, "<textfile.txt> or <url>: Bulk download from text file containing links")                                              # './bulkfile.txt' or 'https://somesite.com'
    UNZIP = (('-u', '--unzip'), 0, Services.BASIC, ": Enables unzipping of files automatically, requires 7z and setup to be done correctly")                                    # True to unzip, false to no unzip
    HTTPS_CODES = (('-z', '--http_codes'), 4, Services.BASIC, "\"500, 502,...\" : HTTP codes to retry downloads on, default is 429 and 403")                                   # [500, 502]
    HTTPS_RETRIES = (('-r', '--http_retries'), 1, Services.BASIC, "<#> : Maximum number of HTTP code retries, default is infinite")                                           # 100 for 100 retries
    HELP = (('-h',), -1, Services.BASIC, ": Help")                                                                                                                                # Display help options and halt program execution
    
    # KEMONO SPECIAL CONFIG ##########################################################################
    KEMONO_FNAME_TYPE = (('--kxftype',), 2, Services.KEMONO, "<download format> : Custom file name, tokens-> [#] counter, [server] -> server name")                               #'[#] - [server]' or '[#]' or [server]
    KEMONO_EXCLUDE_FILE = (('--kxfile',), 3, Services.KEMONO, "\"txt, zip, ..., png\" : Exclude files with listed extensions, NO '.'s")                                           #'['png', 'jpg']'
    KEMONO_EXCLUDE_POST = (('--kxpost',), 3, Services.KEMONO, "\"keyword1, keyword2,...\" : Keyword in excluded posts, not case sensitive")                                       #'['2021', 'hello']'
    KEMONO_EXCLUDE_LINK = (('--kxlink',), 3, Services.KEMONO, "\"keyword1, keyword2,...\" : Keyword in excluded link, not case sensitive. Is for link plaintext, not its target") #'['clip', 'mega']'
    KEMONO_FILE_STRUCTURE = (('--kfstructure',), 1, Services.KEMONO, "<#> : 0 for packed, 1 for partial unpacked, 2 for unpacked")                                                #'0 = packed, 1 = partial, 2 = unpacked'
    

def get_all_config()->list[tuple]:
    """
    Returns all configs

    Returns:
        list[tuple]: All configs
    """
    return [c.value for c in Config]

def print_help()->None:
    """
    Prints help information about how to use switches
    """
    configs = get_all_config()
    buffer = "Switch details\n"
    for config in configs:
        # Process tuple of switches
        for i,n in enumerate(config[0]):
            # print switch
            buffer += ("{switch}{space}".format(switch=n, space = ", "))
        # Process description
        buffer += "{d}\n".format(d=config[3])
    
    logging.info(buffer)