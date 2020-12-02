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
        del fuzzing[5]
        del fuzzing[6]
    elif input_key is 'lastname' or input_key is 'firstname':
        del fuzzing[0]
        del fuzzing[1]
    elif input_key is 'mail':
        del fuzzing[2]
    elif input_key is 'password':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[2]
        del fuzzing[7]
    elif input_key is 'street_number':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[2]
        del fuzzing[7]
    elif input_key is 'country' or input_key is 'town' \
            or input_key is 'street' or input_key is 'region' \
            or input_key is 'postal_code':
        del fuzzing[0]
        del fuzzing[1]
        del fuzzing[7]
    return fuzzing


def get_token_template():
    return {
            "client_id": "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
            "client_secret": "test",
            "grant_type": "password",
            "app_id": "arlex-ccevqe",
            "username": "john@doe.com",
            "password": "password"
        }

def get_form_template(new_user):
    return {
            'state': "AMXHz3TJp9asTcwX21jl2YfbTE7i3Ou0m--bj4QylQ-wRm6llYEmP12v7vH5T0Z1burSoWW6gszPTsfhDdSG_0t9RmRF0msF1w6jnKl4lLRHYerPZh_VBjm0h9aEJsUbglgGsQBSdTqUJB0RjJgXG1zXma_I3oomoSZQlo1pZWTtMsOLNLtkNU-Dqr_10m4GF7NPIu6XYj7ZReFyUpSleOeKn__vB8mnmYcCyWw1YcpGMHIZ9PHgVgF5Fm04SvAnZIxGEaMscF1mQdRZv6YTr0PZurzvdMcJVBIUshjVrQLasfCMzrMuekHFHfaSKHPQepL1tuSgws8blDXKGs4oCJxoENlKZpn7yZVc_59DnSu_8dwLbIcrW1GfqRujw87kJERa0jxJEAb99-4YK7Vxahjlfq5PYf_kfkq5-CiGs2m2a7LwP3p4Ljg7uDiB4ND1bEpKVm_2R1GYEOn540GOBsyUKZcgTIqb0M7spOXGxdVMYdLLqv9waOzHNM8kCJbMM2tWIzhGAflfJV2tVW7AGuULzKVMkTnQv6hGOc13-9w0J3taX-hZJDo",
            'client_id': "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
            'response_type': "code",
            'redirect_uri': "https://oauth-redirect.googleusercontent.com/r/arlex-ccevqe",
            'scope': "",
            'username': new_user['mail'],
            'password': new_user['password']
        }
def print_arg(arg):
    print("try with : {} '{}'".format(type(arg), arg))
