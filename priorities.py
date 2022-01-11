import datetime as dt
from datetime import datetime, timedelta
from enum import Enum

class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Goal:
    def __init__(self, g_id:int, description:str, creation_date:datetime,
                 status:Status, termination_date:datetime):
        self.g_id = g_id
        self.description = description
        self.creation_date = creation_date
        self.status = status
        self.termination_date = termination_date

class Interest:
    def __init__(self, i_id:int, description:str, creation_date:datetime,
                 last_interaction:datetime, status:Status,
                 termination_date:datetime):
        self.i_id = i_id
        self.description = description
        self.creation_date = creation_date
        self.last_interaction = last_interaction
        self.status = status
        self.termination_date = termination_date

class Reminder:
    def __init__(self, r_id:int, description:str, expiration_date:datetime,
                 expected_time:timedelta, creation_date:datetime, status:Status,
                 completion_date:datetime):
        self.r_id = r_id
        self.description = description
        self.expiration_date = expiration_date
        self.expected_time = expected_time
        self.creation_date = creation_date
        self.status = status
        self.completion_date = completion_date
