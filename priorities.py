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
    """
    Basic class to encapsulate data for a Remidner as stored in universe.
    """
    def __init__(self, r_id:int, description:str, expiration:datetime,
                 expected_time:timedelta, creation_date:datetime, status:Status,
                 complete_time:datetime):
        self.r_id = r_id
        self.description = description
        self.expiration = expiration
        self.expected_time = expected_time
        self.creation_date = creation_date
        self.status = status
        self.complete_time = complete_time

    def __repr__(self):
        return ("Reminder(r_id : {}, description : {}, expiration : {}, expected_time : {}, creation_date : {}, ".format(
            self.r_id, self.description, self.expiration,
            self.expected_time, self.creation_date) + "status : {}, complete_time : {})".format(
            self.status, self.complete_time))
