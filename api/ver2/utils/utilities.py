from api.ver1.utils import error


def system_unavailable(e):
    print('Runtime Exception: ' + e.args[0])
    return error(
        message='System unavailable, please try again later!',
        code=500
    )
