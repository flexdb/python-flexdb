# FlexDB (Python)

FlexDB is a flexible, free-to-use database service that allows for instant and seamless integration through its REST API. This library, `python-flexdb`, provides an easy-to-use Python wrapper around the [FlexDB](https://flexdb.co) REST API.

[![github stars](https://img.shields.io/github/stars/flexdb/py-flexdb)](https://github.com/flexdb/py-flexdb) [![pypi version](https://img.shields.io/pypi/v/flexdb)](https://pypi.org/project/flexdb) [![pypi downloads](https://img.shields.io/pypi/dm/flexdb)](https://pypi.org/project/flexdb) [![license](https://img.shields.io/pypi/l/flexdb)](LICENSE.md)

## Installation

To start using FlexDB in your project, simply run the following command:

```bash
pip install python-flexdb
```

## Usage

### Importing the library

First, let's import the `FlexDB` class from the `flexdb` package:

```python
from python-flexdb import FlexDB
```

### Initialize FlexDB

Now, create a new instance of the `FlexDB` class.

```python
flexdb = FlexDB()
```

You can pass an optional configuration dictionary containing your API key and the API endpoint:

```python
flexdb = FlexDB({'api_key': 'your_api_key'})
```

### Create a store

A store is like a container for your data. To create a new store, call the `create_store` method with a unique name:

```python
store = await flexdb.create_store('my-store')
```

### Get a store

To fetch an existing store by its name (when using an API key), use the `get_store` method:

```python
store = await flexdb.get_store('my-store')
```

### Ensure a store exists

If you want to make sure a store exists before performing any operations, use the `ensure_store_exists` method. It will return the existing store or create a new one if it doesn't exist:

```python
store = await flexdb.ensure_store_exists('my-store')
```

### Create a collection

A collection is a group of related documents within a store. To create a new collection, call the `collection` method on a store instance:

```python
collection = store.collection('my-collection')
```

Note: no collection will be created until you add a document to it.

### Create a document

To add a new document to a collection, use the `create` method and pass an object containing the data you want to store:

```python
document = await collection.create({'key': 'value'})
```

### Get a document

To fetch a document by its ID, use the `get` method:

```python
document = await collection.get('document_id')
```

### Update a document

To update an existing document, call the `update` method with the document ID and an object containing the updated data:

```python
updated_document = await collection.update('document_id', {'key': 'new_value'})
```

### Delete a document

To remove a document from a collection, use the `delete` method and pass the document ID:

```python
await collection.delete('document_id')
```

### Get many documents

To fetch multiple documents from a collection, use the `get_many` method. You can pass an options dictionary to control pagination and the number of documents to fetch:

```python
documents = await collection.get_many({'page': 1, 'limit': 10})
```

### Delete a collection

To remove an entire collection and all its documents, call the `delete_collection` method:

```python
await collection.delete_collection()
```

### Delete a store

To delete a store and all its collections, use the `delete` method on a store instance:

```python
await store.delete()
```

## License

This project is licensed under the GPL-3.0 License - see the [[[LICENSE.md```(LICENSE.md) file for details.
