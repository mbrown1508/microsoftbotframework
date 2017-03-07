__author__ = 'Matthew'
from configparser import ConfigParser
import os

def ConfigSectionMap(section):
    config = ConfigParser()
    config.read('{}\config.ini'.format(os.getcwd()))
    return {key : value for key,value in config[section].items()}