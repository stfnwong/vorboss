# Interacts with airtable
from typing import Any, Dict, List, Optional
import datetime     # maybe can be narrower later
from dateutil import parser

from pyairtable import Api


def get_token_from_file(filename:str="token.txt") -> str:
    with open(filename, "r") as fp:
        token = fp.read().strip()

    return token



def pc_date_string_to_dt(date_str:str) -> datetime.datetime:
    return parser.parse(date_str)

def dt_to_pc_date_string(dt:datetime.datetime) -> str:
    time_format = "%d/%m/%Y"
    return dt.strftime(time_format)


class AirtableClient:
    def __init__(self, api_token:str, base_id:str, table_id:str, fields:Optional[Dict[str, str]]=None):
        self.base_id = base_id
        self.table_id = table_id
        self.fields = fields

        # Get an airtable api object
        # TODO: what do we catch on fail?
        self.api = Api(api_token)

    def get_fields(self) -> List[str]:
        return list(self.fields.keys())


    def get(self, max_records:int=100, fields:Optional[List[str]]=None) -> List[Dict[str, Any]]:
        if not fields:
            fields = self.get_fields()

        return self.api.all(self.base_id, self.table_id, fields=fields, max_records=max_records)


    # TODO: continue the pagination
    def get_as_df(self, max_records:int=100, fields:Optional[List[str]]=None) -> List[Dict[str, Any]]:
        if not fields:
            fields = self.get_fields()

        api_return = self.api.all(
            self.base_id, self.table_id, fields=fields, max_records=max_records
        )
        return pd.DataFrame(
            [elem["fields"] for elem in api_return],
            columns=fields
        )
