import json
from collections import Counter

def get_failed_login_user(line_dict):
    if line_dict['eventid'] == "cowrie.login.failed":
        return line_dict['username']
    else:
        return False

def get_failed_login_ip(line_dict):
    if line_dict['eventid'] == "cowrie.login.failed":
        return line_dict['src_ip']
    else:
        return False

def get_successful_login_user(line_dict):
    if line_dict['eventid'] == 'cowrie.login.success':
        return line_dict['username']
    else:
        return False

def get_login_attempt_password(line_dict):
    if line_dict['eventid'] == 'cowrie.login.success' or line_dict['eventid'] == "cowrie.login.failed":
        return line_dict['password']
    else:
        return False

def most_frequent(list):
    occurrences = Counter(list)
    return occurrences.most_common(1)[0][0]

def top_ten(list):
    occurrences = Counter(list)
    top_ten_dict = occurrences.most_common(10)
    top_ten_string = top_ten_dict[0][0] + ", " + top_ten_dict[1][0] + ", " + top_ten_dict[2][0] + ", " + top_ten_dict[3][0] + ", " +top_ten_dict[4][0] + ", " + top_ten_dict[5][0] + ", " + top_ten_dict[6][0] + ", " + top_ten_dict[7][0] + ", " + top_ten_dict[8][0] + ", " + top_ten_dict[9][0]
    return top_ten_string


def main():
    file = open('honey.log', 'r')
    lines = file.readlines()

    failed_login_list = []
    failed_ip_list = []
    successful_login_list = []
    passwords_list = []

    for line in lines:
        line_dict = json.loads(line)

        failed_login_user = get_failed_login_user(line_dict)
        failed_login_ip = get_failed_login_ip(line_dict)
        successful_login_user = get_successful_login_user(line_dict)
        login_attempt_password = get_login_attempt_password(line_dict)

        if (failed_login_user != False):
            failed_login_list.append(failed_login_user)
        if (failed_login_ip != False):
            failed_ip_list.append(failed_login_ip)
        if (successful_login_user != False):
            successful_login_list.append(successful_login_user)
        if (login_attempt_password != False):
            passwords_list.append(login_attempt_password)

    print("Number of failed logins:", len(failed_login_list))
    print("Most common failed login username:", most_frequent(failed_login_list))
    print("Number of successful logins:", len(successful_login_list))
    print("Most common successful login username:", most_frequent(successful_login_list))
    print("Source IP with the most unsuccessful login attempts:", most_frequent(failed_ip_list))
    print("Top ten attempted passwords:", top_ten(passwords_list))


main()