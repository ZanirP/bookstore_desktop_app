import requests

class APIClient:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000/"
        self.token = None

    def _auth_header(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, username, password):
        url = self.base_url + "/auth/login"

        response = requests.post(url,
                                 json = {"username": username,
                                         "password": password
                                })

        return response.json()

    def get_all_books(self):
        url = self.base_url + "/books/"
        return requests.get(url, headers=self._auth_header()).json()

    def search_books(self, query):
        url = self.base_url + f"/books/search?q={query}"
        return requests.get(url, headers=self._auth_header()).json()

    def get_book_details(self, book_id):
        url = self.base_url + f"/books/{book_id}"
        return requests.get(url, headers=self._auth_header()).json()

    def checkout(self, cart_items):
        url = self.base_url + "/orders"
        return requests.post(url,
            json={"items": cart_items},
            headers=self._auth_header()
        ).json()

    def get_reviews(self, book_id):
        url = self.base_url + f"/books/{book_id}/reviews"
        return requests.get(url, headers=self._auth_header()).json()

    def get_all_orders(self):
        url = self.base_url + "/orders/all"
        return requests.get(url, headers=self._auth_header()).json()

    def update_order_status(self, order_id, status):
        url = self.base_url + f"/orders/{order_id}/status"
        return requests.patch(url, json={"payment_status": status}, headers=self._auth_header()).json()

    def add_book(self, data):
        url = self.base_url + "/books"
        return requests.post(url, json=data, headers=self._auth_header()).json()

    def update_book(self, book_id, data):
        url = self.base_url + f"/books/{book_id}"
        return requests.patch(url, json=data, headers=self._auth_header()).json()

    def register(self, username, password, email):
        url = self.base_url + "/auth/register"
        return requests.post(url, json={
            "username": username,
            "password": password,
            "email": email
        }).json()

    def logout(self):
        url = self.base_url + "/auth/logout"
        return requests.post(url, headers=self._auth_header()).json()


api = APIClient()