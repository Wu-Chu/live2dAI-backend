
def get_json_result(retcode=0, retmsg='success', data=None):
    result_dict = {
        "retcode": retcode,
        "retmsg": retmsg,
        "data": data,
    }

    return result_dict


def get_error_json_result(retcode=500, retmsg='success', data=None):
    result_dict = {
        "retcode": retcode,
        "retmsg": retmsg,
        "data": data,
    }

    return result_dict
