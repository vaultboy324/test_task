import os
import json

from constants import client_parameters
from constants import template_names

from modules.database_requests import DatabaseRequests


class GetSelector:
    _DEFAULT_CLIENT_PATH = os.getcwd() + chr(92) + 'client' + chr(92)

    @staticmethod
    def _format_data(data):
        json_str = json.dumps(data)
        return json_str.encode(encoding='utf-8')

    @staticmethod
    def _get_file(path: str, client_catalog: str, file_name: str):
        file = open(path +
                    client_catalog +
                    chr(92) +
                    file_name,
                    encoding='utf-8').read()
        return bytes(file, 'utf-8')

    @staticmethod
    def _get_json(url_params: list):
        if url_params[client_parameters.ENTITY_TYPE] == client_parameters.REGIONS_PATH:
            regions = DatabaseRequests.get_regions()
            return GetSelector._format_data(regions)

        elif url_params[client_parameters.ENTITY_TYPE] == client_parameters.CITIES_PATH:
            if len(url_params) == 3:
                cities = (DatabaseRequests.
                          get_cities_by_region(url_params[client_parameters.PARAMETER_TYPE]))
                return GetSelector._format_data(cities)

        elif url_params[client_parameters.ENTITY_TYPE] == client_parameters.COMMENT_PATH:
            comments = DatabaseRequests.get_comments()
            return GetSelector._format_data(comments)

        elif url_params[client_parameters.ENTITY_TYPE] == client_parameters.STAT_PATH:
            region_stat = DatabaseRequests.get_region_stat()
            return GetSelector._format_data(region_stat)

        elif url_params[client_parameters.ENTITY_TYPE] == client_parameters.CITIES_STAT_PATH:
            if len(url_params) == 3:
                cities_stat = (DatabaseRequests.
                               get_cities_stat_by_region(url_params[client_parameters.PARAMETER_TYPE]))
                return GetSelector._format_data(cities_stat)

    @staticmethod
    def get_data(url: str):
        try:
            path = os.environ.get('DEFAULT_CLIENT_PATH',
                                  GetSelector._DEFAULT_CLIENT_PATH)

            params = url.split('/')[1:]
            if params[client_parameters.RESOURCE_TYPE] == '':
                params[client_parameters.RESOURCE_TYPE] = client_parameters.VIEW_PATH

            if url.endswith(client_parameters.JS):
                return GetSelector._get_file(path,
                                             client_parameters.JS,
                                             params[client_parameters.ENTITY_TYPE])

            elif url.endswith(client_parameters.CSS):
                return GetSelector._get_file(path,
                                             client_parameters.CSS,
                                             params[client_parameters.ENTITY_TYPE])

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.DATA:
                return GetSelector._get_json(params)

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.FAVICON:
                return GetSelector._format_data({})

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.COMMENT_PATH:
                if len(params) > 1:
                    raise Exception
                return GetSelector._get_file(path,
                                             client_parameters.TEMPLATES,
                                             template_names.comment)

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.VIEW_PATH:
                if len(params) > 1:
                    raise Exception
                return GetSelector._get_file(path,
                                             client_parameters.TEMPLATES,
                                             template_names.view)

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.STAT_PATH:
                if len(params) > 1:
                    raise Exception
                return GetSelector._get_file(path,
                                             client_parameters.TEMPLATES,
                                             template_names.stat)

            elif params[client_parameters.RESOURCE_TYPE] == client_parameters.CITIES_STAT_PATH:
                if len(params) > 2:
                    raise Exception
                return GetSelector._get_file(path,
                                             client_parameters.TEMPLATES,
                                             template_names.cities_stat)
        except Exception:
            return None
