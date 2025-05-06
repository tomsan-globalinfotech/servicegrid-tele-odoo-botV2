from enum import Enum

class TimesheetStates(Enum):
    PROJECT_SELECT = 1
    TASK_SELECT = 2
    DURATION_ENTRY = 3
    DESCRIPTION_ENTRY = 4
    CONFIRMATION = 5