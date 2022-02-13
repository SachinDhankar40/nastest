
def error_message(error_key):
    '''
        provides the custom exception statements.
    '''
    error_dict = {
        "E_01":"User limit exceeded.",
        "E_02":"slot_number doesn't exists.",
        "E_03":"car_number should start with alphabet.",
        "E_04":"car_number contains invalid character.",
        "E_05":"car_number should be alpha numeric.",
        "E_06":"car_number is already parked.",
        "E_07":"all parking slots are filled.",
        "E_08":"wrond datatype provided."
    }
    return error_dict.get(error_key)


def success_message(success_key):
    '''
        provides the custom success statements.
    '''
    success_dict = {
        "S_01":"Successfuly unparked.",
        "S_02":"Successfuly parked."
    }
    return success_dict.get(success_key)