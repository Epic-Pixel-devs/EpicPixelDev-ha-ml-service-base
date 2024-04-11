# -*- coding: utf-8 -*-
import json
import os
import sys
import urllib.request as ur

sys.path.append(os.path.abspath(os.getcwd()))

from services.pymongo_service import PymongoService
from domain.valorant.model.agents_model import AgentsModel
from services.log.log_service import LogService
from services.environment.build_env_service import BuildEnvService

# storage path root and some constants variables
AGENTS = 'agents'
VALORANT = 'valorant'
DOMAIN = 'domain'
INFRA = 'infra'
SERVER = 'server'
MONGO = 'mongo'

ROOT_PATH = os.path.join(os.getcwd())
STORAGE_PATH = f'{ROOT_PATH}/storage'
VALORANT_PATH = f'{STORAGE_PATH}/{VALORANT}'
VALORANT_FILE_PATH = f'{VALORANT_PATH}/files'
VALORANT_IMAGE_PATH = f'{VALORANT_PATH}/images'


def insert_data(db, collection_name, data) -> None:
    """
    description:
        this method is responsible to make insert into database
    args:
        collection_name (str): name of MongoDb collection
        data (any): data which will be inserted
    see: 
        https://www.mongodb.com/pt-br/docs/manual/reference/method/db.collection.insert/
    """

    LogService.log().info(f'[batch valorant] (insert_data): insert into database')
    db[collection_name].insert_one(vars(data))


def build_model_valorant(data) -> AgentsModel:
    """
    description:
        this method is responsible to make parse string from data coming valorant
        and return new instance of AgentsModel
    args:
        data (any): result from valorant http response
    return:
         AgentsModel
    """
    LogService.log().info(f'[batch valorant] (build_model_valorant): create new instance AgentsModel')
    return AgentsModel(json.dumps(json.loads(data)))


def get_data(url: str) -> str:
    """
    description:
        this method is responsible to make http call on api valorant and get some data
    args:
        url (str): URL to make http call
    return:
        http response from valorant and convert to string
    """
    LogService.log().info(f'[batch valorant] (getData): request open url')
    response = ur.urlopen(url)

    LogService.log().info(f'[batch valorant] (getData): read reponse http')
    byte_data = response.read()

    LogService.log().info(f'[batch valorant] (getData): convert chartset to utf-8')
    encoding = response.info().get_content_charset('utf8')

    LogService.log().info(f'[batch valorant] (getData): return data string')
    return byte_data.decode(encoding)


def create_dir():
    """
    description:
        this method is responsible to create some dirs if not extis
    """
    LogService.log().info(f'[batch valorant] (create_dir): create some dirs if not exists')
    for directory in [VALORANT_PATH, VALORANT_FILE_PATH, VALORANT_IMAGE_PATH]:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


def initialize():
    LogService.log().info(f'[batch valorant] (initialize): check connection database')
    assert PymongoService().get_mongo_client().admin.command('ping')

    LogService.log().info(f'[batch valorant] (initialize): load some variables config')
    env = BuildEnvService().load_environment(f'{ROOT_PATH}/application.yml')

    valorant = env.get(DOMAIN).get(VALORANT)
    mongo = env.get(INFRA).get(MONGO)

    LogService.log().info(f'[batch valorant] (initialize): create some dirs if not exists')
    create_dir()

    LogService.log().info(f'[batch valorant] (initialize): loading instance mongodb')
    mongo_instance = PymongoService.get_instance()

    LogService.log().info(f'[batch valorant] (initialize): create some dirs if not exists')
    non_db = mongo_instance.get_db(f'{mongo.get("database").get("names")[0]}')

    """
    see:
        https://stackoverflow.com/questions/72323776/find-only-specific-key-from-mongodb-using-pymongo
        https://stackoverflow.com/questions/6570371/when-to-use-and-when-to-use-is
    """
    LogService.log().info(f'[batch valorant] (initialize): fetch all {AGENTS} from database')
    agents_list = list(non_db[VALORANT].find({AGENTS: {'$exists': True}}))

    LogService.log().info(f'[batch valorant] (initialize): check if list agents if bigger than zero')
    if len(agents_list) <= 0:
        insert_data(VALORANT,
                    build_model_valorant(
                            get_data(f'{valorant.get("url")}/{AGENTS}')))
    else:
        LogService.log().info(f'[batch valorant] (initialize): some data founded doing validation')
        for agent in agents_list:
            ag = AgentsModel(json.dumps(agent.get(AGENTS)))
            if ag.hash_validator != agent.get('hash_validator'):
                # make request to valorant to get new informations
                try:
                    insert_data(VALORANT,
                                build_model_valorant(
                                        get_data(f'{valorant.get("url")}/{AGENTS}')))
                except Exception as e:
                    LogService.log().error(f'[batch valorant] (initialize): {str(e)}')
            else:
                LogService.log().info(f'[batch valorant] (initialize): {AGENTS} already registered.')


if __name__ == '__main__':
    initialize()
