import requests

class APIClient:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000/"
        self.token = None

    def login(self, username, password):
        url = self.base_url + "/auth/login"

        response = requests.post(url,
                                 json = {"username": username,
                                         "password": password
                                })

        return response.json()



api = APIClient()