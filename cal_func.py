# Functionality to make calls to Google Calendar API
import datetime
import requests
import os
from datetime import datetime
from typing import Dict

def get_freebusy(access_token:str, timeMin:str, timeMax:str,
                 timeZone:str, cal_id:str):
    """
    Make freebusy query to Google Calendar API to return freebusy info. 

    timeMin and timeMax may or may not in the future get passed in another
    format. Likely will be some time offset, but for now using this since
    dynamic user time choice has not been implemented yet. It will soon though
    :)

    Parameters
    ==========
    access_token : str
        Access token required to authenticate with the Google Authorization server
    timeMin : str 
        The beginning time bound to consider
    timeMax : str 
        The ending time bound to consider
    timeZone : str
        Timezone for request 
    cal_id : str
        ID of the calendar to query 

    Returns
    =======
    freebusy_info : Dict 
        Freebusy info formatted per
        https://developers.google.com/calendar/api/v3/reference/freebusy/query
    """
    request_url = "https://www.googleapis.com/calendar/v3/freeBusy"
    bearer = f"Bearer {access_token}"
    headers = {"Authorization" : bearer,
               "Accept" : "application/json",
               "Content-Type" : "application/json"}
    data = '{"timeMin":"' + f'{timeMin}","timeMax":"{timeMax}",'\
           '"timeZone":"' + f'{timeZone}",'\
           '"items":[{"id":"' + f'{cal_id}"' + '}]}'
    api_key = os.environ["GOOGLE_API_KEY"] 
    params = {"key" : api_key} 
    req = requests.post(request_url, headers=headers, data=data, params=params) 
    freebusy_info = req.text
    
    return freebusy_info 

def get_time_available(freebusy_info:Dict, cal_id:str):
    """
    Gets hours available from freebusy info with given calendar id.

    Parameters
    ==========
    freebusy_info : Dict
        Dictionary of freebusy information, per Google Calendar API response
        format : https://developers.google.com/calendar/api/v3/reference/freebusy/query
    cal_id : str
        Calendar ID of interest 

    Returns
    =======
    hours : Union[int, float] 
        Hours available
    """
    print(f'Here is freebusy info : {freebusy_info}')
    print(f"Here is type of freebusy info : {type(freebusy_info)}")
    try:
        print("Trying to index right in")
        busy_info = freebusy_info["calendars"][cal_id]["busy"]
        print(f"Busy info : \n {busy_info}")
    except Exception as exp:
        print("Indexing in does not work, try something else")
        print(f"Exception: {exp}")

    try:
        print("Trying to convert to dictionary first")
        freebusy_dct = freebusy_info.to_dict()
        busy_info = freebusy_info["calendars"][cal_id]["busy"]
        print(f"Busy info : \n {busy_info}")
    except Exception as exp:
        print("Converting to dictionary first doesn't work, try something else")
        print(f"Exception: {exp}")
