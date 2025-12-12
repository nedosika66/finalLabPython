import requests
import json

class NetworkHelper:
    BASE_URL = "http://127.0.0.1:8001/api/"
    AUTH = ('norata66', 'NaZaR123!')

    def __init__(self):
        pass

    def get_list(self, endpoint):
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}/", auth=self.AUTH)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error: {e}")
        return []

 
    def delete_item(self, endpoint, item_id):
        try:
            response = requests.delete(f"{self.BASE_URL}{endpoint}/{item_id}/", auth=self.AUTH)
            return response.status_code == 204
        except Exception as e:
            print(f"Error: {e}")
            return False


    def get_item(self, endpoint, item_id):
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}/{item_id}/", auth=self.AUTH)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error: {e}")
        return None

    def create_item(self, endpoint, data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f"{self.BASE_URL}{endpoint}/", 
                auth=self.AUTH, 
                data=json.dumps(data), 
                headers=headers
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error: {e}")
            return False

    def update_item(self, endpoint, item_id, data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.put(
                f"{self.BASE_URL}{endpoint}/{item_id}/", 
                auth=self.AUTH, 
                data=json.dumps(data), 
                headers=headers
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False