API_ERRORS = {
    'auth.AuthorizationTypeError': {
        'errorCode': 0,
        'msg': 'Invalid authorization type'
    },
    'auth.CredentialsValidationError': {
        'errorCode': 1,
        'msg': 'Could not validate credentials'
    },
    'auth.InvalidFingerPrint': {
        'errorCode': 2,
        'msg': 'Invalid fingerPrint'
    },
    'auth.InvalidToken': {
        'errorCode': 3,
        'msg': 'Invalid token'
    },
    'auth.MissingRefreshToken': {
        'errorCode': 4,
        'msg': 'Missing refresh token'
    },
    'auth.RefreshTokenExpired': {
        'errorCode': 5,
        'msg': 'Refresh token expired'
    },
    'file.FileIsNotAnImage': {
        'errorCode': 6,
        'msg': 'File is not an image'
    },
    'password.InvalidPassword': {
        'errorCode': 7,
        'msg': 'Invalid password'
    },
    'password.MustContainDigits': {
        'errorCode': 8,
        'msg': 'Password must contain digits'
    },
    'password.MustContainUppercase': {
        'errorCode': 9,
        'msg': 'Password must contain uppercase characters'
    },
    'password.WrongLength': {
        'errorCode': 10,
        'msg': 'Password must contain at least 8 characters'
    },
    'project.AlreadyExists': {
        'errorCode': 11,
        'msg': 'Project with this title already exists'
    },
    'project.NoAccess': {
        'errorCode': 12,
        'msg': "Don't have access to this project"
    },
    'project.NotFound': {
        'errorCode': 13,
        'msg': 'Project not found'
    },
    'user.AlreadyExists': {
        'errorCode': 14,
        'msg': 'User already exists'
    },
    'user.NotFound': {
        'errorCode': 15,
        'msg': 'User not found'
    },
    'username.InvalidUsername': {
        'errorCode': 16,
        'msg': 'Invalid username'
    },
    'username.WrongFormat': {
        'errorCode': 17,
        'msg': 'Wrong username format'
    },
    'auth.NotAuthenticated': {
        'errorCode': 18,
        'msg': 'Not authenticated'
    },
    'skillTag.NotUnique': {
        'errorCode': 19,
        'msg': 'All skill tags must be unique'
    },
    'skillTag.Required': {
        'errorCode': 20,
        'msg': 'Minimum one skill tag need to be specified'
    },
    'username.ToShort': {
        'errorCode': 21,
        'msg': 'Username must contain at least 8 characters'
    },
    'password.WrongFormat': {
        'errorCode': 22,
        'msg': 'Wrong password format'
    }
}
