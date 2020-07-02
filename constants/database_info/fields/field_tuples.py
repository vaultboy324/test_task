from . import region_fields
from . import cities_fields
from . import comment_fields
from . import other_fields

FIELDS_FOR_COMMENT_TABLE = (comment_fields.ID, comment_fields.SURNAME,
                            comment_fields.NAME, comment_fields.FATHER_NAME,
                            other_fields.REGION, other_fields.CITY,
                            comment_fields.PHONE, comment_fields.EMAIL,
                            comment_fields.COMMENT_TEXT)

FIELDS_FOR_REGION_STAT = (region_fields.ID, other_fields.REGION, other_fields.COUNT)

FIELDS_FOR_CITIES_STAT = (other_fields.REGION, other_fields.CITY, other_fields.COUNT)
