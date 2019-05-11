from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    @task
    def get_movies(self):
        self.client.get("/movies?genre=Science+Fiction&offset=0&limit=10")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
