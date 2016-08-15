
CODE_MSG = {
    # Base code
    0  : 'OK.',
    1  : 'Server maintenance.',
    2  : 'API Version error.', # use in middleware
    
    # User
    30000 : 'Account created successfully.',
    30001 : 'Account exists.',
    30002 : 'Mobile phone number or password error.',
    30003 : 'Account not exists.',
    30004 : 'Join token is not available.',
    30005 : "Parent's level reach limit, can not have children.",
    30006 : "User's account has not passed verify.",

    # Service
    30100 : 'IM service request error.',
    30101 : 'SMS code verify error.',
    30102 : 'SMS code daily count limit reached.',
    30103 : 'SMS code send error.',
}
