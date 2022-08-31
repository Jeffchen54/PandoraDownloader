from enum import Enum
import logging
import time


class Service(Enum):
    """
    Service supported by PandoraDownloader
    Each member value is associated with its class instance name
    For example, Service.Kemono = KemonoComponent.
    Author: Jeff Chen
    Date: 8/29/2023
    # TODO add component
    """
    BASIC = 0
    KEMONO = 1


class Config(Enum):
    """
    Configurations and settings supported by Pandora. Each member value
    is associated with an integer which describes which value should be
    passed in to manipulate a configuration and the switch association
    with the config and class associated with the config
    and a description of the config.

    Member value format example:
    Config.A_CONFIG = (("--SWITCH USED", "-s"), 1, Service.BASIC, "Does this")

    Format dissection:
    Tuple[Tuple[str], int, Service.value, str]

    Outer tuple always size 2, inner tuple always at least size 1

    Integer value for a config:
    -1: help
    0: bool
    1: int, need to process next token
    2: str, need to process next token
    3: list[str], need to process next token, input type is a comma separated list, need to convert to lower case
    4: list[int], need to process next token, input type is a comma separated list
    5: str, need to process next token, input type is a file with absolute path
    6: str, need to process next token, input type is a directory with absolute path

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
    # './' or '../' or '../folder/file.txt' or 'C:/user/folder'
    DOWNLOAD_FOLDER = (('-d', '--download_folder'), 6, Service.BASIC,
                       "<path> : REQUIRED - Set download path for single instance, must use '\\' or '/'")
    # 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all
    VERBOSE = (('-v', '--verbose'), 1, Service.BASIC,
               ": 0 for no output, 1 for important info, 2 for important info and warnings, 3 for all")
    # 6 for six threads
    THREAD_COUNT = (('-t', '--threads'), 1, Service.BASIC,
                    "<#> : Change download thread count (default is 6)")
    # 6400000 for ~64MBs
    DOWNLOAD_CHUNK_SZ = (('-c', '--chunk_sz'), 1, Service.BASIC,
                         "<#> : Adjust download chunk size in bytes (Default is 64M)")
    # './bulkfile.txt' or 'https://somesite.com'
    DOWNLOAD_URL = (('-f', '--bulk'), 5, Service.BASIC,
                    "<textfile.txt> or <url>: Bulk download from text file containing links")
    # True to unzip, false to no unzip
    UNZIP = (('-u', '--unzip'), 0, Service.BASIC,
             ": Enables unzipping of files automatically, requires 7z and setup to be done correctly")
    # [500, 502]
    HTTPS_CODES = (('-z', '--http_codes'), 4, Service.BASIC,
                   "\"500, 502,...\" : HTTP codes to retry downloads on, default is 429 and 403")
    # 100 for 100 retries
    HTTPS_RETRIES = (('-r', '--http_retries'), 1, Service.BASIC,
                     "<#> : Maximum number of HTTP code retries, default is infinite")
    # Display help options and halt program execution
    HELP = (('-h',), -1, Service.BASIC, ": Help")

    # KEMONO SPECIAL CONFIG ##########################################################################
    # '[#] - [server]' or '[#]' or [server]
    KEMONO_FNAME_TYPE = (('--kxftype',), 2, Service.KEMONO,
                         "<download format> : Custom file name, tokens-> [#] counter, [server] -> server name")
    KEMONO_EXCLUDE_FILE = (('--kxfile',), 3, Service.KEMONO,
                           "\"txt, zip, ..., png\" : Exclude files with listed extensions, NO '.'s")  # '['png', 'jpg']'
    KEMONO_EXCLUDE_POST = (('--kxpost',), 3, Service.KEMONO,
                           "\"keyword1, keyword2,...\" : Keyword in excluded posts, not case sensitive")  # '['2021', 'hello']'
    KEMONO_EXCLUDE_LINK = (('--kxlink',), 3, Service.KEMONO,
                           "\"keyword1, keyword2,...\" : Keyword in excluded link, not case sensitive. Is for link plaintext, not its target")  # '['clip', 'mega']'
    # '0 = packed, 1 = partial, 2 = unpacked'
    KEMONO_FILE_STRUCTURE = (('--kfstructure',), 1, Service.KEMONO,
                             "<#> : 0 for packed, 1 for partial unpacked, 2 for unpacked")


def get_all_config() -> list[tuple]:
    """
    Returns all configs

    Returns:
        list[tuple]: All configs
    """
    return [c.value for c in Config]


def print_help() -> None:
    """
    Prints help information about how to use switches
    May seem inefficient to create help buffer each invocation; however
    help is usually printed just once and then the program quits out. 
    """
    configs = get_all_config()
    buffer = "Switch details\n"
    for config in configs:
        # Process tuple of switches
        for _, n in enumerate(config[0]):
            # print switch
            buffer += ("{switch}{space}".format(switch=n, space=", "))
        # Process description
        buffer += "{d}\n".format(d=config[3])

    logging.info(buffer)


def __fixed_format_generator(initial):
    """
    Returns a formatter which aids in formatting data in get_dict_table.

    Param:
        initial: initial value of formatter 
    Return: formatter function
    """
    counter = initial

    def formatter(switches: tuple, data: int, service):
        """
        Formats input data into the following format:
        [(switch, (counter, data, service)),...]

        where multiple switches may exists; however, all switches
        passed in will have the same counter. 

        After each call to format, counter increments by 1

        Args:
            switch (tuple): tuple of switches
            data (int): value manipulation integer in Switches.value
            service (Service.value): service type associated with switches

        Returns:
            list: list containing each switch with formatted data
        """
        # can't be done in one line due to python lacking post increment operator
        nonlocal counter
        formatted = [(switch, (counter, data, service)) for switch in switches]
        counter += 1
        return formatted
    return formatter


def get_switch_to_info_table() -> dict:
    """
    Generates a dict table for all config switches as key and a tuple containing config id, 
    value to pass in, and related service as value, if a Config.value has multiple
    switches, multiple entries in the dict table will exists. 

    Example of dict table:
    {
        "-d" : (0, 2, Service.BASIC),
        "--download_folder" : (0, 2, Service.BASIC)
        ...
    }

    KV structure:
    "switch" : (id:int, data_type:int, Service:Service.value)

    "switch": what switch the KVpair is associated with
    id: switch config identifier, switches that do the same thing have the same id
    data_type: data to send for config, more details in Config enum in this file
    Service: What service the switch is associated with.

    Returns:
        dict: all config switches and a tuple containing config id, 
        value to pass in, and related service as value,
    """
    formatter = __fixed_format_generator(0)
    dict_table = [elem for inner in [formatter(switches, data, service) for (
        switches, data, service, description) in get_all_config()] for elem in inner]

    return (dict(dict_table))


def get_switch_to_config_table() -> dict:
    """
    Generates a dict table for all config switches as key and value containing 
    which Config.value is associated with the switch. If a Config.value has multiple
    switches, multiple entries in the dict table will exists. 

    Example of a dict table
    {
        "-d" : Config.AConfig,
        "--download_folder" : Config.AConfig
        ...
    }

    KV structure:
    "switch" : Config.value

    "switch": what switch the KVpair is associated with
    Config.value: Config.value the switch is associated with

    Returns:
        dict: all config switches with their associated Config.value
    """
    dict_table = list()

    for config in get_all_config():
        for switch in config[0]:
            dict_table.append((switch, config))
    return dict(dict_table)
