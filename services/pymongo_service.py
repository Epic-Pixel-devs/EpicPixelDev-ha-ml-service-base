# -*- coding: utf-8 -*-
import pymongo


class PymongoService:
    instance = None

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            'mongodb+srv://herdeiros_aurora:herdeiros_aurora_001@cluster0.otugy2g.mongodb.net/')

    def get_db(self, db_name: str):
        """
        Responsible to get database, need to pass in parameter the name of database
        which you want to connect.

        Args:
            db_name (str): name of database
        """
        return self.client[db_name]

    def get_mongo_client(self):
        """
        Responsible to get mongo client after connect on database
        """
        return self.client

    @staticmethod
    def get_instance():
        """
        Responsible to create new instance of class PytMongo if not exists
        """
        if not PymongoService.instance:
            PymongoService.instance = PymongoService()
        return PymongoService.instance
