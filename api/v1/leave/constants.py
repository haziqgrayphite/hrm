from enum import Enum


class RoleChoices(Enum):
    OWNER = 'Owner'
    ADMIN = 'Admin'
    HR = 'HR'
    EMPLOYEE = 'Employee'
    TEAM_LEAD = 'Team-Lead'
    NOT_SPECIFIED = 'None'
