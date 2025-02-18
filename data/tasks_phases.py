from enum import StrEnum

class TaskPhases(StrEnum):
    TODO = 'To Do'
    PROGRESS = 'In Progress'
    FINISH = 'Done'

    @classmethod
    def get_all_phases(cls):
        return [task.value for task in cls]