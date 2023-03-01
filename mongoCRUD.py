from pymongo import MongoClient
from configurations import AppConfig
from loguru import logger


class MongoConnect:
    def __init__(self, db: str):
        """
        Initializes the mongo connection

        :param db: Database name to connect (act as default db)
        """
        url = AppConfig().getMongoUrl()
        self.mongo = MongoClient(url)
        self.db = db

    def fetchDat(self, col: str, query: dict, args: dict = None, db: str = None) -> list:
        """
        Provides a list of documents that match.

        :param col: collection name
        :param query: query to fetch the data
        :param args: [Optional] Specifies the exclusion of a field
        :param db:  [Optional] default metadb
        :return: [List] fetched data based on the query (list of dictionary[object])
        """
        try:
            args = dict() if args is None else args
            db = db if db is not None else self.db
            return list(self.mongo[db][col].find(query, args))
        except Exception as err:
            logger.error(err)
            return []

    def insertDat(self, col: str, query: dict, db: str = None) -> None:
        """
        Inserts the data in mongo collection

        :param col: Collection Name
        :param query: Query to insert in the collection
        :param db: [Optional] Database name, default = initialized db
        :return: [None] returns None
        """
        try:
            db = db if db is not None else self.db
            self.mongo[db][col].insert_one(query)
        except Exception as err:
            logger.error(err)

    def updateDat(self, col: str, query: dict, data: dict, db: str = None, upsert: bool = False) -> None:
        """
        Updates the document, if document not present inserts the document

        :param upsert: if a record isn't found, inserts one
        :param col: Collection Name
        :param query: Query to fetch document
        :param data: data to update
        :param db: [Optional] Database Name, default = Initialized database
        :return: [None] returns None
        """
        try:
            db = db if db is not None else self.db
            self.mongo[db][col].update_one(query, {'$set': data}, upsert=upsert)
        except Exception as err:
            logger.error(err)

    def deleteDat(self, col: str, query: dict, db: str = None) -> None:
        """
        Deletes a document from a collection

        :param col: Collection Name
        :param query: Query to delete document
        :param db: [Optional] Database name, default = Initialised db
        :return: [None] returns None
        """
        try:
            db = db if db is not None else self.db
            self.mongo[db][col].delete_one(query)
        except Exception as err:
            logger.error(err)

    def listDatabases(self, db: str = None):
        """
        Get a list of all the collection names in this database.

        :param db: database name
        """
        try:
            db = db if db is not None else self.db
            return self.mongo[db].list_collection_names()

        except Exception as err:
            logger.error(err)

    def bulkWrite(self, db: str = None, col: str = None, data: list = None):
        """
        Send a batch of write operations to the server.
        :param db: db name
        :param col: collection name
        :param data:  data to be written
        """

        try:
            db = db if db is not None else self.db
            self.mongo[db][col].bulk_write(data)
        except Exception as err:
            logger.error(err)
