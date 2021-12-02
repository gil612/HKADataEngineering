""" Configuration Handler. """
import copy
import json
import logging
import os
import traceback

from flask import current_app

CONFIGFILES = {'config.json'}

class Configuration():
    def __init__(self, default):
        self._config = copy.deepcopy(default)
        try:
            self._config = current_app.config
        except:
            logging.warning("Couldn't read config from Flask.current_app.")

    def __getitem__(self,key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self._config[key] = value

    def __contains__(self,key):
        return key in self._config

    def get(self,key):
        if key not in self._config:
            logging.error('Key "%s" not present in config', key)
            #If an error occurs get the 30 last function inputs
            traceback.print_stack(limit=30)
            return None
        return self._config[key]
    
    def get_default(self, key, default=None):
        """ Return value for key, using default if key doesn't exist """
        if key not in self._config:
            logging.warning('Key "%s" is not present in config!', key)
            return default
        return self._config[key]

    def get_dict(self):
        """Return a handle to the full config dict. """
        return self._config

    def parse_arg(self, arg):
        """ Parse an argument of the form 'key=value' """
        key = arg[:arg.find('=')]
        val = arg[arg.find('=') + 1:]
        self._config[key] = val

    def parse_args(self, args):
        for arg in args:
            self.parse_arg(arg)

    def read_configfiles(self, configfiles=CONFIGFILES):
        """ Read configuration from multiple JSON files. """
        for configfile in configfiles:
            self.read_configfile(configfile)

    def read_configfile(self,configfile):
        if not os.path.isfile(configfile):
            logging.warning('Config file %s does not exist in %s', configfile, os.getcwd)
            return
        logging.info('Reading config file %s', configfile)
        self._config.update(json.loads(open(configfile).read()))


    def get_config_dict(self):
        return self._config
        
#EOF
