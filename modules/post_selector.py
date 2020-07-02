import json

from constants import client_parameters
from modules.database_requests import DatabaseRequests


class PostSelector:
    @staticmethod
    def do_method(url: str, post_data):
        params = url.split('/')[1:]

        new_row = json.loads(post_data.decode())

        if params[client_parameters.RESOURCE_TYPE] == client_parameters.COMMENT_PATH:
            DatabaseRequests.post_comment(new_row)
        else:
            return
