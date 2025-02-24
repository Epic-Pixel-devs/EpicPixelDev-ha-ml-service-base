# -*- coding: utf-8 -*-

import os
import re

import yaml
from dotenv import load_dotenv

from services.log.log_service import LogService

load_dotenv()

log = LogService.log()


class BuildEnvService:
    """
    see:
        https://dev.to/mkaranasou/python-yaml-configuration-with-environment-variables-parsing-2ha6
    """
    def __init__(self):
        log.info(f"[BuildEnvService] (parse_config): starting parse config")
        log.info(f'[BuildEnvService] (parse_config): pattern for global vars: look for word')
        self.pattern = re.compile(r'.*?\${(\w+)}.*?')

    def load_environment(self, path, data=None, tag=''):
        """
        Load a yaml configuration file and resolve any environment variables
        The environment variables must have !ENV before them and be in this format
        to be parsed: ${VAR_NAME}.

        database:
            host: !ENV ${HOST}
            port: !ENV ${PORT}
        app:
            log_path: !ENV '/var/${LOG_PATH}'
            something_else: !ENV '${AWESOME_ENV_VAR}/var/${A_SECOND_AWESOME_VAR}'
        :param str path: the path to the yaml file
        :param str data: the yaml data itself as a stream
        :param str tag: the tag to look for
        :return: the dict configuration
        :rtype: dict[str, T]
        """

        log.info(f'[BuildEnvService] (parse_config): yml safe loader open file')
        loader = yaml.SafeLoader

        # the tag will be used to mark where to start searching for the pattern
        # e.g. some key: !ENV some string${MYENVVAR}blah blah blah
        log.info(f'[BuildEnvService] (parse_config): add implicit resolver')
        loader.add_implicit_resolver(tag, self.pattern, None)
        loader.add_constructor(tag, self.constructor_env_variables)

        if path:
            with open(path) as file:
                return yaml.load(file, Loader=loader)
        elif data:
            return yaml.load(data, Loader=loader)
        else:
            raise ValueError('Either a path or data should be defined as input')

    def constructor_env_variables(self, loader, node):
        """
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = self.pattern.findall(value)  # to find all environment variables in line

        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(f'${{{g}}}', os.environ.get(g, g))
            return full_value
        return value
