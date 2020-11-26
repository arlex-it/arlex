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
    if input_key is 'id_ean' or input_key is 'position' or input_key is 'id_arlex':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[2]
        del fuzzing[7]
    return fuzzing


def print_arg(arg):
    print("try with : {} '{}'".format(type(arg), arg))
