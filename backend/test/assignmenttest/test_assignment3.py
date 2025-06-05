
import pytest
import pymongo
from src.util.dao import DAO
from dotenv import dotenv_values
import os
LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

@pytest.fixture
def test_db():
    client = pymongo.MongoClient(MONGO_URL)
    db = client["test_db"]
    collection = db["test_collection"]
    yield collection
    collection.drop()
    client.close()

def test_dao_insert(test_db):
    dao = DAO("task")
    insert_data = {"title": "testing", "description": "testing integration"}
    created_doc = dao.create(insert_data)
    id_str = created_doc["_id"]["$oid"]
    found_doc = dao.findOne(id_str)
    expected_doc_after_find = {"_id": {"$oid": id_str}}
    for key, value in insert_data.items(): # Add all inserted data to expected
        expected_doc_after_find[key] = value    

    assert found_doc == expected_doc_after_find

def test_dao_insert_invalid(test_db):
    dao = DAO("task")
    insert_data = {"title": "testing without description"}
    with pytest.raises(pymongo.errors.WriteError): # More specific exception
        dao.create(insert_data)


#Testar date med bokstäver
def test_invalid_date_type(test_db):
    dao = DAO("task")
    insert_data = {"title": "testing", "description": "testing integration", "startdate": "blabla", "duedate": "blabla"}
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(insert_data)

#testar samma titel, title är uniqueitem
def test_same_title(test_db):
    dao = DAO("task")
    insert_data1 = {"title": "testing", "description": "testing integration1"}
    dao.create(insert_data1)
    insert_data2 = {"title": "testing", "description": "testing integration2"}
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(insert_data2)

def test_invalid_title(test_db):
    dao = DAO("task")
    insert_data_wrong_type_title = {"title": 12345, "description": "description here"}
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(insert_data_wrong_type_title)