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
    freebusy_info = req.json()
    
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
    time_available : Union[int, float] 
        Time available in hours 
    """
    busy_times = freebusy_info["calendars"][cal_id]["busy"]
    print(f"Busy Times : {busy_times}")
    dt_format = "%Y-%m-%dT%H:%M:%S%z"
    # Imagine if you had the whole day.
    time_available = 24 
    for time_pair in busy_times:
        start = time_pair['start']
        end = time_pair['end']
        start_dt = datetime.strptime(start, dt_format)
        end_dt = datetime.strptime(end, dt_format)
        delta = end_dt - start_dt
        busy = delta.total_seconds() / 3600
        # You'd hope this is positive
        if delta > 0: 
            time_available -= busy 
        else:
            print(f"Somehow got a negative busy time : {busy}")
    print(f"Time available : {time_available}")
    return time_available
