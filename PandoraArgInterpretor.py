from Services import Services

"""
Interprets command line arguments used for
PandoraDownloader 
Author: Jeff Chen
Date: 8/29/2022
"""

def interpret(args:list[str])->dict[Services,tuple[str]]:
    """
    Processes command line arguments and sends 
    back instructions in dict form that can be understood
    by PandoraDownloader.

    Args:
        args result from returning sys.argv or equivalent: 
    Return: dict of the form {"service1":tuple, "service2":tuple...}
        service are member values of Services and tuple is 
        ["settingStr":param, "settingStr2":param]
    """