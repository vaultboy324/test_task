from constants import client_parameters

from modules.database_requests import DatabaseRequests


class DeleteSelector:
    @staticmethod
    def delete_row(url: str):
        params = url.split('/')[1:]

        if params[client_parameters.RESOURCE_TYPE] == client_parameters.COMMENT_PATH:
            comment_id = params[client_parameters.ENTITY_TYPE]
            DatabaseRequests.delete_comment(comment_id)
