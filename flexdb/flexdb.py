# Copyright (C) 2023 FlexDB <team@flexdb.co>
# Use of this source code is governed by the GPL-3.0
# license that can be found in the LICENSE file.

import requests

class FlexDB:
    def __init__(self, config = {}):
        self.api_key = config.get('apiKey', '')
        self.base_url = config.get('endpoint', 'https://flexdb.co/api/v1')

    def headers(self, context):
        headers = {'Authorization': ''}
        if context == 'account':
            if self.api_key and len(self.api_key) > 0:
                headers['Authorization'] = f'Account {self.api_key}'
        else:
            headers['Authorization'] = f'Store {context}'

        if len(headers['Authorization']) > 0:
            return headers

    def requests_call(self, method, url, data = None, headers_context = None):
        try:
            response = requests.request(method, self.base_url + url, headers=self.headers(headers_context), json=data)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as err:
            if err.response.status_code == 404:
                return None
            else:
                raise err

    # def requests_call(self, method, url, data = None, headers_context = None):
    #     try:
    #         response = requests.request(method, self.base_url + url, headers=self.headers(headers_context), json=data)
    #         response.raise_for_status()
    #         json_response = response.json()
    #         print(f"Response received: {json_response}")
    #         return json_response
    #     except requests.HTTPError as err:
    #         print(f"HTTPError encountered: {err}")
    #         print(f"Response was: {err.response.text}")
    #         if err.response.status_code == 404:
    #             return None
    #         else:
    #             raise err
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         raise e

    def create_store(self, name):
        response_data = self.requests_call('POST', '/stores', {'name': name}, 'account')
        return Store(self, response_data)

    def get_store(self, name):
        try:
            response_data = self.requests_call('GET', f'/stores/{name}', headers_context='account')
            return Store(self, response_data)
        except Exception:
            return None

    def get_stores(self):
        response_data = self.requests_call('GET', '/stores', headers_context='account')
        return [Store(self, store) for store in response_data]

    def ensure_store_exists(self, name):
        store = self.get_store(name)
        if not store:
            return self.create_store(name)
        return store


class Store:
    def __init__(self, flexdb, data):
        self.data = data
        self.id = data['id']
        self.flexdb = flexdb

    def collection(self, name):
        return Collection(self, name)

    def delete(self):
        return self.flexdb.requests_call('DELETE', f'/stores/{self.data["id"]}', headers_context=self.data['id'])


class Collection:
    def __init__(self, store, name):
        self.name = name
        self.store = store

    def delete_collection(self):
        return self.store.flexdb.requests_call('DELETE', f'/collections/{self.name}', headers_context=self.store.id)

    def create(self, data):
        return self.store.flexdb.requests_call('POST', f'/collections/{self.name}', data, self.store.id)

    def get_many(self, options = {}):
        params = {key: value for key, value in options.items() if key in {'page', 'limit', 'skip'}}
        if 'page' in params and 'skip' in params:
            raise Exception('Cannot use page and skip together')

        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        return self.store.flexdb.requests_call('GET', f'/collections/{self.name}?{query_string}', headers_context=self.store.id)

    def get(self, id):
        return self.store.flexdb.requests_call('GET', f'/collections/{self.name}/{id}', headers_context=self.store.id)

    def update(self, id, data):
        return self.store.flexdb.requests_call('PUT', f'/collections/{self.name}/{id}', data, self.store.id)

    def delete(self, id):
        return self.store.flexdb.requests_call('DELETE', f'/collections/{self.name}/{id}', headers_context=self.store.id)
