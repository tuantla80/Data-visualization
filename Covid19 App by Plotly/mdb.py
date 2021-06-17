'''
Purpose: To build a MongoDB database: mdb.py  (mdb: Mongo Database)
'''
import datetime
import sys
import os
import pandas as pd
from pymongo import MongoClient


class MongoDB:
    '''
    To access, upload to and download from MongoDB
    '''
    def __init__(self,
                 host,
                 port,
                 db_name=None,
                 collection_name=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name


    def get_client(self):
        '''To get mongo client'''
        return MongoClient(self.host, self.port)


    def get_db(self):
        '''To get db object of the current db name
        NOTE: When calling this function, MongoDB will create the database if it does not exist,
              and make a connection to it.
        Eg. import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client['new_db']  # if new_db is not existed, it will create "new_db" database
        '''
        return self.get_client()[self.db_name]


    def get_dbs(self):
        '''To get list of db names in MongoDB including system db'''
        return self.get_client().list_database_names()


    def get_collection(self):
        '''To get collection object of current collection name'''
        return self.get_db()[self.collection_name]


    def get_collection_names(self, include_system_collections=False):
        '''To get list of all collection names in the current db object
        :param include_system_collections: True if include system collections else False
        '''
        return self.get_db().list_collection_names(include_system_collections=include_system_collections)


    def find(self, query=None):
        '''To find info. in a collection
        :param query:
            Eg 1.   host, port = '127.0.0.1', 27017
                    db_name, collection_name = 'test', 'my_collection'
                    mongodb = MongoDB(host, port, db_name, collection_name)

                    query = {'x': 8}
                    cursor = mongodb.find(query)
                    for doc in cursor:
                        print(doc)
                    Output:
                    {'_id': ObjectId('608264e5af7ffba348c5f4c0'), 'x': 8}

            Eg 2.   query = {}  # find all
                    cursor = mongodb.find(query)
                    for doc in cursor:
                        print(doc)
                    Output:
                    {'_id': ObjectId('608264c9af7ffba348c5f4bf'), 'x': 10}
                    {'_id': ObjectId('608264e5af7ffba348c5f4c0'), 'x': 8}
                    {'_id': ObjectId('608264edaf7ffba348c5f4c1'), 'x': 11}
        :return:
        '''
        query = query or {}
        cursor = self.get_collection().find(query)
        return cursor


    def upload_df(self, df):
        '''To upload a df to MongoDB
        :param df: a Pandas Dataframe
        Eg.
        host, port = '127.0.0.1', 27017
        db_name, collection_name = 'test', 'my_collection'
        mongodb = MongoDB(host, port, db_name, collection_name)

        df = pd.DataFrame({'a': [1, None], 'b': ['b1', 'b2']})
        print(df.to_string())
        print('upload df')
        mongodb.upload_df(df=df)

        Output:
        DataFrame
             a   b
        0  1.0  b1
        1  NaN  b2
        upload df
        The below two documents have been uploaded in MongoDB
        {'_id': ObjectId('608f70db462b01a8c1b7701c'), 'a': 1.0, 'b': 'b1'}
        {'_id': ObjectId('608f70db462b01a8c1b7701d'), 'a': nan, 'b': 'b2'}
        '''
        self.get_db()[self.collection_name].insert_many(df.to_dict(orient='records'))
        return None


    def upload_dics(self, dics):
        '''To upload a list of dicts to MongoDB
        :param dics:
            dics here are equivalent to df.to_dict(orient='records') as in upload_df()
        :return:

        Note:
        bson.errors.InvalidDocument: key 'Single Cells/Single Cells/live/LC and Mono/LC/non BT/CD15neg/NK 1 | Freq. of LC' must not contain '.'
        '''
        self.get_db()[self.collection_name].insert_many(dics)
        return None


    def download_df(self, query=None, limit=None, no_id=True, projection=None):
        '''To download data from MongoDB and store into a df

        :param query:
        :param limit: number of documents to be returned
        :param no_id:
        :param projection:
            Eg. projection = {'a': 1, 'b': 1}
        :return:
        '''
        query = query or {}
        projection = projection or {}

        _db = self.get_db()
        if not limit:
            if projection:
                cursor = _db[self.collection_name].find(query, projection)
            else:
                cursor = _db[self.collection_name].find(query)
        else:
            if projection:
                cursor = _db[self.collection_name].find(query, projection).limit(limit)
            else:
                cursor = _db[self.collection_name].find(query).limit(limit)
        # End of if not limit
        df = pd.DataFrame(list(cursor))
        if no_id and '_id' in list(df.columns):
            del df['_id'] # Delete the _id

        return df


    def create_single_index(self, keys):
        '''To create single index in a collection
        :param keys:
            Eg. keys=['mfp.idx', 'mfp.count']
        NOTE: ensure_index is deprecated
        :return:
        '''
        assert (isinstance(keys, list) and
                all(isinstance(key, str) for key in keys))
        for key in keys:
            self.get_collection().create_index(key)
        return None


    def create_compound_index(self, keys):
        '''To create compound index in a collection
        :param keys:
            Eg. keys = [('pfp.idx', 1), ('pfp.value', 1)]
        :return:
        '''
        assert (isinstance(keys, list) and
                all(isinstance(key, tuple) for key in keys))
        self.get_collection().create_index(keys)
        return None


    def create_text_index(self, keys):
        '''To create text index in a collection
        :param keys:
            Eg. keys = [('pfp_str.idx', 'text')]
        :return:
        '''
        self.get_collection().create_index(keys)
        return None


    def drop_indexes(self, keys):
        '''To drop one or more indexes
        :param keys:
            Eg. keys = ['mfp.idx', 'mfp.count']
        :return:
        '''
        for _index in keys:
            self.get_collection().drop_index(_index)
        return None


    def calculate_index_size(self):
        '''To calculate the size (memory) of indexes
        :return:
        '''
        return self.get_db().command("serverStatus")


    def rename_field_name(self, dic_rename=None):
        '''To rename a field in a collection
        :param dic_rename:
            Eg. dic_rename = {"old_field_name": "new_field_name"}
        :return:
        Eg. dic_rename = {'a': 'modified_a'}
        Data BEFORE in MongoDB
                x    b            a
            0  10.0  NaN         NaN
            1   8.0  NaN         NaN
            2  11.0  NaN         NaN
            3   NaN   b1         1.0
            4   NaN   b2         NaN
        Data AFTER in MongoDB
                x    b           modified_a
            0  10.0  NaN         NaN
            1   8.0  NaN         NaN
            2  11.0  NaN         NaN
            3   NaN   b1         1.0
            4   NaN   b2         NaN
        '''
        dic_rename = dic_rename or {}
        _db = self.get_db()
        _db[self.collection_name].update_many({}, {'$rename': dic_rename})
        return None


    def remove_field_from_document(self, fields=None):
        '''To remove filed from a document
        :param fields:
            Ex. fields=['field_name_1', 'field_name_2']
        :return:
        Eg.  fields=['modified_a']
        Data BEFORE in MongoDB
                x    b           modified_a
            0  10.0  NaN         NaN
            1   8.0  NaN         NaN
            2  11.0  NaN         NaN
            3   NaN   b1         1.0
            4   NaN   b2         NaN
        Data AFTER in MongoDB
                x    b
            0  10.0  NaN
            1   8.0  NaN
            2  11.0  NaN
            3   NaN   b1
            4   NaN   b2
        '''
        fields = fields or []
        for field in fields:
            self.get_collection().update_many({}, {"$unset": {field: 1}})
        return None


def test_MongoDB_class():

    print('Start at', datetime.datetime.now())

    host, port = '127.0.0.1', 27017
    db_name, collection_name = 'test', 'my_collection'
    mongodb = MongoDB(host, port, db_name, collection_name)
    print(f'mongodb = {mongodb}')
    print(f'get_client() method = {mongodb.get_client()}')
    print(f'get_db() method = {mongodb.get_db()}')
    print(f'get_dbs() method = {mongodb.get_dbs()}')
    print(f'get_collection() method = {mongodb.get_collection()}')
    print(f'get_collection_names() method = {mongodb.get_collection_names()}')

    print('find() method')
    cursor = mongodb.find(query={})
    for doc in cursor:
        print(doc)
    print(f'find() = {cursor}, type={type(cursor)}')

    print('DataFrame')
    df = pd.DataFrame({'a': [1, None], 'b': ['b1', 'b2']})
    print(df.to_string())
    print('upload_df() method')
    mongodb.upload_df(df=df)
    print('df has been uploaded')

    print('download_df')
    df_downloaded = mongodb.download_df(query={})
    print(f'download_df() = {df_downloaded.to_string()}')

    print('rename_field_name() method')
    mongodb.rename_field_name(dic_rename={'a': 'modified_a'})
    print('get data after changing field name')
    df_downloaded = mongodb.download_df(query={})
    print(f'download_df() =\n {df_downloaded.to_string()}')

    print(f'remove_field_from_document() method')
    mongodb.remove_field_from_document(fields=['modified_a'])
    print('get data after removing field name')
    df_downloaded = mongodb.download_df(query={})
    print(f'download_df() =\n {df_downloaded.to_string()}')

    print('End at', datetime.datetime.now())


if __name__ == "__main__":
    pass