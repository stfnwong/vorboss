# Interacts with airtable
from dateutil import parser
from pyairtable import Api, Table
from pyairtable.formulas import match
from typing import Any, Dict, List, Optional
import datetime     # maybe can be narrower later
import pandas as pd


def get_token_from_file(filename:str="token.txt") -> str:
    with open(filename, "r") as fp:
        token = fp.read().strip()

    return token



def pc_date_string_to_dt(date_str:str) -> datetime.datetime:
    return parser.parse(date_str)

def dt_to_pc_date_string(dt:datetime.datetime) -> str:
    time_format = "%d/%m/%Y"
    return dt.strftime(time_format)


# Some methods to create formula expressions for filtering  
def create_date_range_formula(field_id:str, start_date:str, end_date:str) -> str:
    return f"AND(IS_AFTER \"{field_id}\" \"{start_date}\") IS_BEFORE( \"{field_id}\" \"{end_date}))\""


# TODO: clean this up, this is just some extra formula stuff
from pyairtable.formulas import FIND, STR_VALUE, FIELD



class AirtableClient:
    def __init__(self, api_token:str, base_id:str, table_id:str, fields:Optional[Dict[str, str]]=None):
        """
        Create a new client to access the airtable backend.

        api_token (str): A token with at least read access to the airtable backend.

        base_id (str) : Airtable base id

        table_id (str): Id for this table

        fields (Optional[Dict[str, str]]) : Mapping of field names to field ids.

        """

        self.base_id = base_id
        self.table_id = table_id
        self.fields = fields

        # Get an airtable api object
        # TODO: what do we catch on fail?
        self.api = Api(api_token)
        self.table = Table(api_token, self.base_id, self.table_id)

    def get_fields(self) -> List[str]:
        try:
            return list(self.fields.keys())
        except Exception:
            return []

    def get(self, max_records:int=100, fields:Optional[List[str]]=None) -> List[Dict[str, Any]]:
        if not fields:
            fields = self.get_fields()

        return self.api.all(self.base_id, self.table_id, fields=fields, max_records=max_records)


    # TODO: continue the pagination
    def get_as_df(
        self,
        max_records:int=0,
        formula=None,
        fields:Optional[List[str]]=None
    ) -> pd.DataFrame:
        if not fields:
            fields = self.get_fields()

        #records = [page["fields"] for page in record for record in self.api.iterate(self.base_id, self.table_id, fields=fields, max_records=max_records)]
        records = []
        # TODO: to get the id as well, we would have to do something like
        #for record in page:
        #    records.append(record["fields"] + record["id"])

        if formula:
            records = self.table.first(formula=formula)
            return pd.DataFrame(records)

        for page in self.api.iterate(self.base_id, self.table_id, fields=fields, max_records=None if max_records == 0 else max_records):
            for record in page:
                records.append(record["fields"])

        return pd.DataFrame(records)

        #return pd.DataFrame(
        #    [elem["fields"] for elem in api_return],
        #    columns=fields
        #)
