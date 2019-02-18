# Return Status Codes
STATUS_CODE_POST_SUCCESS = 204
STATUS_CODE_GET_SUCCESS = 200
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_SERVER_ERROR = 500

# Standard Return Messages
MSG_EMPTY_RESPONSE = ''

# Return Messages for Registration
MSG_REGISTRATION_WRONG_INPUT = 'Wrong input. Expecting {"teacher": <email>, "students": [<email>, <email>, ...]}'
MSG_REGISTRATION_SERVER_ERROR = 'Failed to add new registration. Please check that the registration does not already exist.'

# Return Messages for Listing Common Students
MSG_LIST_STUDENTS_WRONG_INPUT = 'Wrong input. Expecting {"teacher": [<email>, <email>, ...]'
MSG_LIST_STUDENTS_SERVER_ERROR = 'Failed to list common students.'

# Return Messages for Suspending Student
MSG_SUSPENSION_WRONG_INPUT = 'Wrong input. Expecting {"student": <email>}'
MSG_SUSPENSION_SERVER_ERROR = 'Failed to suspend student.'

# Return Messages for Notifying Students
MSG_NOTIFY_WRONG_INPUT = 'Wrong input. Expecting {"teacher": <email>, "notification": <text>}'
MSG_NOTIFY_SERVER_ERROR = 'Failed to retrieve students for notifications.'