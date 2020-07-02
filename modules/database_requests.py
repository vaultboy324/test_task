import sqlite3
import os

from constants.database_info import table_names
from constants.database_info import region_fields
from constants.database_info import comment_fields
from constants.database_info import cities_fields
from constants.database_info import other_fields
from constants.database_info import field_tuples


class DatabaseRequests:
    _DEFAULT_DATABASE_PATH = os.getcwd() + chr(92)
    _DEFAULT_DATABASE_NAME = 'comments.db'
    _DEFAULT_COUNT_FOR_STAT = 5

    @staticmethod
    def _create_connection():
        path = os.environ.get('DEFAULT_DATABASE_PATH',
                              DatabaseRequests._DEFAULT_DATABASE_PATH)
        name = os.environ.get('DEFAULT_DATABASE_NAME',
                              DatabaseRequests._DEFAULT_DATABASE_NAME)

        return sqlite3.connect(path + name)

    @staticmethod
    def _response_to_json(response, ordered_fields):
        result = []

        for element in response:
            row = {}
            for index in range(0, len(element)):
                row[ordered_fields[index]] = element[index]
            result.append(row)

        return result

    @staticmethod
    def _create_insert_request(new_row: dict, ordered_fields: tuple, table_name: str):
        fields_info = f'INSERT INTO {table_name}('
        values_info = f'VALUES('

        for field in ordered_fields[1:]:
            fields_info += f"'{field}',"
            values_info += f"'{new_row[field]}',"

        fields_info = fields_info[0: len(fields_info) - 1]
        values_info = values_info[0: len(values_info) - 1]

        fields_info += ') '
        values_info += ');'

        return fields_info + values_info

    @staticmethod
    def get_regions():
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_names.REGIONS}')

        response = cursor.fetchall()

        conn.close()

        result = DatabaseRequests._response_to_json(response,
                                                    region_fields.ORDERED_FIELDS)

        return result

    @staticmethod
    def post_comment(new_comment: dict):
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()

        request = DatabaseRequests._create_insert_request(new_comment,
                                                          comment_fields.ORDERED_FIELDS,
                                                          table_names.COMMENTS)

        cursor.execute(request)

        conn.commit()

        conn.close()

    @staticmethod
    def get_comments():
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        request = (f'SELECT {table_names.COMMENTS}.{comment_fields.ID}, '
                   f'{table_names.COMMENTS}.{comment_fields.SURNAME}, '
                   f'{table_names.COMMENTS}.{comment_fields.NAME}, '
                   f'{table_names.COMMENTS}.{comment_fields.FATHER_NAME}, '
                   f'{table_names.REGIONS}.{region_fields.NAME} AS {other_fields.REGION}, '
                   f'{table_names.CITIES}.{region_fields.NAME} AS {other_fields.CITY}, '
                   f'{table_names.COMMENTS}.{comment_fields.PHONE}, '
                   f'{table_names.COMMENTS}.{comment_fields.EMAIL}, '
                   f'{table_names.COMMENTS}.{comment_fields.COMMENT_TEXT} '
                   f'FROM {table_names.COMMENTS} INNER JOIN {table_names.CITIES} '
                   f'ON {table_names.COMMENTS}.{comment_fields.CITY_ID} = {table_names.CITIES}.{cities_fields.ID} '
                   f'INNER JOIN {table_names.REGIONS} '
                   f'ON {table_names.CITIES}.{cities_fields.REGION_ID} = {table_names.REGIONS}.{region_fields.ID};')

        cursor.execute(request)

        response = cursor.fetchall()

        conn.close()

        result = DatabaseRequests._response_to_json(response,
                                                    field_tuples.FIELDS_FOR_COMMENT_TABLE)

        return result

    @staticmethod
    def get_cities_by_region(region_id: int):
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * '
                       f'FROM {table_names.CITIES} '
                       f'WHERE {cities_fields.REGION_ID} = {region_id}')

        response = cursor.fetchall()

        conn.close()

        result = DatabaseRequests._response_to_json(response,
                                                    cities_fields.ORDERED_FIELDS)

        return result

    @staticmethod
    def delete_comment(comment_id: int):
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table_names.COMMENTS} '
                       f'WHERE {comment_fields.ID} = {comment_id}')

        conn.commit()

    @staticmethod
    def get_region_stat():
        count_for_stat = int(os.environ.get('DEFAULT_COUNT_FOR_STAT', DatabaseRequests._DEFAULT_COUNT_FOR_STAT))

        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        request = (f'SELECT {table_names.REGIONS}.{region_fields.ID}, '
                   f'{table_names.REGIONS}.{region_fields.NAME} AS {other_fields.REGION}, '
                   f'COUNT({table_names.COMMENTS}.{comment_fields.ID}) '
                   f'FROM {table_names.REGIONS} INNER JOIN  {table_names.CITIES} '
                   f'ON {table_names.CITIES}.{cities_fields.REGION_ID} = {table_names.REGIONS}.{region_fields.ID} '
                   f'INNER JOIN {table_names.COMMENTS} '
                   f'ON {table_names.COMMENTS}.{comment_fields.CITY_ID} = {table_names.CITIES}.{comment_fields.ID} '
                   f'GROUP BY {other_fields.REGION} '
                   f'HAVING COUNT({table_names.COMMENTS}.{comment_fields.ID}) > {count_for_stat}')

        cursor.execute(request)

        response = cursor.fetchall()

        conn.close()

        result = DatabaseRequests._response_to_json(response,
                                                    field_tuples.FIELDS_FOR_REGION_STAT)
        return result

    @staticmethod
    def get_cities_stat_by_region(region_id):
        conn = DatabaseRequests._create_connection()
        cursor = conn.cursor()
        request = (f'SELECT {table_names.REGIONS}.{region_fields.NAME} AS {other_fields.REGION}, '
                   f'{table_names.CITIES}.{comment_fields.NAME} AS {other_fields.CITY}, '
                   f'COUNT({table_names.COMMENTS}.{comment_fields.ID}) '
                   f'FROM {table_names.COMMENTS} INNER JOIN {table_names.CITIES} '
                   f'ON {table_names.COMMENTS}.{comment_fields.CITY_ID} = {table_names.CITIES}.{cities_fields.ID} '
                   f'INNER JOIN {table_names.REGIONS} '
                   f'ON {table_names.CITIES}.{cities_fields.REGION_ID} = {table_names.REGIONS}.{region_fields.ID} '
                   f'WHERE {table_names.REGIONS}.{region_fields.ID} = {region_id} '
                   f'GROUP BY {other_fields.REGION}, {other_fields.CITY}')

        cursor.execute(request)

        response = cursor.fetchall()

        conn.close()

        result = DatabaseRequests._response_to_json(response,
                                                    field_tuples.FIELDS_FOR_CITIES_STAT)
        return result
