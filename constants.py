from enum import Enum


class TimeUnit(Enum):
    DAYS = 1
    WEEKS = 2
    MONTHS = 3
    YEARS = 4
    HOURS = 5
    MINUTES = 6
    SECONDS = 7


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class Persmission(str, Enum):
    CREATE = "d_write"
    READ = "d_read"
    UPDATE = "d_edit"
    DELETE = "d_delete"


class Module(Enum):
    REAL_ESTATE = 1
    HR = 2
    ESS = 3
    CRM = 4
    SALES = 5
    PURCHASING = 6
    ACCOUNTING = 7
    INVENTORY = 8
    GYMS = 9
    CLINICS = 10


# class Feature(Enum):
#     PAYROLL = 1
#     SALARIES = 2
#     ATTENDANCE = 3
#     EMPLOYEE = 4
#     HOLIDAYS = 5


class Feature(Enum):
    LEADS = 1
    ACTIONS = 2
    PROJECTS = 3
    COMPANY_OC = 4
    USER_ROLES = 5
    EMPLOYEES = 6
    DEVELOPERS = 7
    SETTINGS = 8


# class HRFeature(Enum):
#     PAYROLL = 1
#     SALARIES = 2
#     ATTENDANCE = 3
#     EMPLOYEE = 4
#     HOLIDAYS = 5


# class ESSFeature(Enum):
#     SALARIES = 2
#     ATTENDANCE = 3
#     EMPLOYEE = 4


# class SalesFeature(Enum):
#     ACCOUNTS = 1
#     RFQ = 2
#     QUOTATIONS = 3
#     WORK_ORDERS = 4
#     PRODUCTS = 5


class ExistingAction(Enum):
    RAISE = 1
    IGNORE = 2
    UPDATE = 3


class ClockingType(Enum):
    FIXED = 1
    ROTATIONAL = 2


class AttendanceType(Enum):
    ON_SITE = 1
    REMOTE = 2
    HYBRID = 3
    NO_ATTENDANCE = 4


class AdjustmentCategory(Enum):
    REWARDS = 1
    PENALTIES = 2
    ALLOWANCES = 3
    DEDUCTIONS = 4
    SALARY_HOLD = 5
