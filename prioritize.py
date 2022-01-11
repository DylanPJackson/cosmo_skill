from typing import Union, Dict, Tuple, List
from priorities import Goal, Interest, Reminder

def prioritize(time_available:Union[int,float], goals:List[Goal],
               interests:List[Interest], reminders:List[Reminder]):
    """
    Determine how much time to spend on which priorities.

    Parameters
    ==========
    time_available : Union[int, float]
        How much time you have to work with
    goals : List[Goal]
        List of Goals
    interests : List[Interest]
        List of Interests
    reminders : List[Reminder]
        List of Reminders

    Returns
    =======
    itemized_priorities : Dict[str, List[Tuple[str, Union[int, float]]]]
    """
    pass

def main():
    pass 

if __name__ == "__main__":
    main()
