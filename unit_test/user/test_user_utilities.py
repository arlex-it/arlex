def get_fuzzing_data_by_input(input_key):
    fuzzing = {
        0: 'abc',
        1: 'a' * 252,
        2: 'john@doe.com',
        3: -2,
        4: 1,
        5: 99,
        6: 10000000000000,
        7: '10'
    }
    if input_key is 'gender':
        del fuzzing[4]
    elif input_key is 'lastname' or input_key is 'firstname' \
            or input_key is 'country' or input_key is 'town' \
            or input_key is 'street' or input_key is 'region':
        del fuzzing[0]
        del fuzzing[1]
    elif input_key is 'mail':
        del fuzzing[2]
    elif input_key is 'password':
        del fuzzing[3]
        del fuzzing[4]
        del fuzzing[5]
        del fuzzing[6]
    elif input_key is 'street_number':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[7]
    elif input_key is 'postal_code':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[7]
    return fuzzing


def print_arg(arg):
    print("try with : {} '{}'".format(type(arg), arg))
