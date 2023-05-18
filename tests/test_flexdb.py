# Copyright (C) 2023 FlexDB <team@flexdb.co>
# Use of this source code is governed by the GPL-3.0
# license that can be found in the LICENSE file.

# Note: these tests require a running FlexDB instance to be available at the
# endpoint specified in the environment variable FLEXDB_ENDPOINT. If this
# variable is not set, the tests will default to http://localhost:8000.

import os
import pytest
from dotenv import load_dotenv
from flexdb.flexdb import FlexDB, Store

# Load environment variables
load_dotenv()
FLEXDB_API_KEY = os.getenv('FLEXDB_API_KEY')
FLEXDB_ACCOUNT_ID = os.getenv('FLEXDB_ACCOUNT_ID')
FLEXDB_ENDPOINT = os.getenv('FLEXDB_ENDPOINT', 'http://localhost:8000')

# Create FlexDB instances
config = {'endpoint': FLEXDB_ENDPOINT}
authConfig = {'apiKey': FLEXDB_API_KEY, 'endpoint': FLEXDB_ENDPOINT}
flexdb = FlexDB(config=config)
flexdbAuth = FlexDB(config=authConfig)

# Set up and tear down test environment
@pytest.fixture(scope='module', autouse=True)
def setup_teardown():
    print('\n(Setting up test environment)')
    delete_all_stores()
    yield  # this is where the testing happens
    print('\n(Tearing down test environment)')
    delete_all_stores()

# Helper functions
def delete_all_stores():
    print('(Deleting all account stores)')
    stores = flexdbAuth.get_stores()
    for store in stores:
        print(f"(Deleting store {store.data['name']})")
        store.delete()

# Tests
def test_create_store():
    store = flexdb.create_store('test-store')
    assert isinstance(store, Store)
    assert store.data['id'] is not None
    assert store.data['name'] == 'test-store'

def test_create_store_account_association():
    storeAuth = flexdbAuth.create_store('test-store-auth')
    assert isinstance(storeAuth, Store)
    assert storeAuth.data['id'] is not None
    assert storeAuth.data['name'] == 'test-store-auth'
    assert storeAuth.data['account'] == FLEXDB_ACCOUNT_ID

def test_get_store_by_name():
    storeAuth = flexdbAuth.get_store('test-store-auth')
    assert isinstance(storeAuth, Store)
    assert storeAuth.data['id'] is not None
    assert storeAuth.data['name'] == 'test-store-auth'
    assert storeAuth.data['account'] == FLEXDB_ACCOUNT_ID

def test_get_nonexistent_store():
    storeAuth = flexdbAuth.get_store('test-store-auth-2')
    assert storeAuth is None

def test_duplicate_store_creation():
    with pytest.raises(Exception) as e_info:
        flexdbAuth.create_store('test-store-auth')
    assert e_info.value.response.status_code == 409

def test_delete_store():
    storeAuth = flexdbAuth.get_store('test-store-auth')
    response = storeAuth.delete()
    assert response['success'] == True

def test_ensure_existing_store_exists():
    store = flexdb.ensure_store_exists('test-store')
    assert isinstance(store, Store)
    assert store.data['id'] is not None
    assert store.data['name'] == 'test-store'

def test_ensure_nonexisting_store_exists():
    store = flexdb.ensure_store_exists('test-store-new-1')
    assert isinstance(store, Store)
    assert store.data['id'] is not None
    assert store.data['name'] == 'test-store-new-1'
    store.delete()

def test_create_new_document_in_collection():
    users = flexdb.create_store('test-store').collection('users')
    user = users.create({'name': 'Alice'})
    assert user['id'] is not None
    assert user['name'] == 'Alice'

def test_get_document_by_id():
    users = flexdb.create_store('test-store').collection('users')
    user = users.create({'name': 'Bob'})
    bob = users.get(user['id'])
    assert bob['id'] == user['id']
    assert bob['name'] == 'Bob'

def test_update_document_by_id():
    users = flexdb.create_store('test-store').collection('users')
    user = users.create({'name': 'Bob'})
    users.update(user['id'], {'name': 'Bobby'})
    bob = users.get(user['id'])
    assert bob['id'] == user['id']
    assert bob['name'] == 'Bobby'

def test_delete_document_by_id():
    users = flexdb.create_store('test-store').collection('users')
    user = users.create({'name': 'Bob'})
    users.delete(user['id'])
    bob = users.get(user['id'])
    assert bob is None

def test_get_non_existent_document():
    users = flexdb.create_store('test-store').collection('users')
    nonExistentUser = users.get('non-existent-id')
    assert nonExistentUser is None

def test_server_unreachable():
    unreachableFlexDB = FlexDB(config={'endpoint': 'http://localhost:9999'})
    with pytest.raises(Exception) as e_info:
        unreachableFlexDB.create_store('test-store')
    assert 'ConnectionError' in str(e_info.value)
