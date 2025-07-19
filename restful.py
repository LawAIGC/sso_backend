
def success(data):
    return {
        "errno": 0,
        "msg": "success",
        "data": data,
    }


def error(msg):
    return {
        "errno": 1,
        "msg": msg,
        "data": {},
    }
