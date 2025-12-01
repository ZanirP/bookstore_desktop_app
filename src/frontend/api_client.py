import requests

class APIClient:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000/"
        self.token = None



api = APIClient()