from api.base_client import BaseClient


class UserEndpoints(BaseClient):
    def __init__(self):
        super().__init__()
        self.users_url = "/users"

    def get_all_users(self):
        return self.get(self.users_url)

    def get_user(self, user_id):
        return self.get(f"{self.users_url}/{user_id}")

    def create_user(self, payload):
        return self.post(self.users_url, payload)

    def update_user(self, user_id, payload):
        return self.put(f"{self.users_url}/{user_id}", payload)

    def delete_user(self, user_id):
        return self.delete(f"{self.users_url}/{user_id}")


class PostEndpoints(BaseClient):
    def __init__(self):
        super().__init__()
        self.posts_url = "/posts"

    def get_all_posts(self):
        return self.get(self.posts_url)

    def get_post(self, post_id):
        return self.post(self.posts_url)

    def create_post(self, payload):
        return self.post(self.posts_url, payload)

    def update_post(self, post_id, payload):
        return self.put(f"{self.posts_url}/{post_id}", payload)

    def delete_post(self, post_id):
        return self.delete(f"{self.posts_url}/{post_id}")