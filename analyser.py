import json
from collections import Counter


def get_failed_login_user(line_dict):
    if line_dict['eventid'] == 'cowrie.login.failed':
        return line_dict['username']
    else:
        return False


def get_failed_login_ip(line_dict):
    if line_dict['eventid'] == 'cowrie.login.failed':
        return line_dict['src_ip']
    else:
        return False


def get_successful_login_user(line_dict):
    if line_dict['eventid'] == 'cowrie.login.success':
        return line_dict['username']
    else:
        return False


def get_login_attempt_password(line_dict):
    if line_dict['eventid'] == 'cowrie.login.success' or line_dict['eventid'] == 'cowrie.login.failed':
        return line_dict['password']
    else:
        return False


def get_source_ips(line_dict):
    return line_dict['src_ip']


def get_unique_successful_root_login_ip(line_dict, unique_ip_list):
    if line_dict['eventid'] == 'cowrie.login.success' and (line_dict['src_ip'] not in unique_ip_list) and line_dict[
        'username'] == 'root':
        return line_dict['src_ip']
    else:
        return False


def check_if_root_login_failed(line_dict):
    if line_dict['eventid'] == 'cowrie.login.failed' and line_dict['username'] == 'root':
        return True
    else:
        return False


def get_after_login_command(line_dict, next_line_dict):
    if line_dict['eventid'] == 'cowrie.login.success':
        return next_line_dict['eventid']
    else:
        return False


def most_frequent(list):
    occurrences = Counter(list)
    return occurrences.most_common(1)[0][0]


def top_ten(list):
    occurrences = Counter(list)
    top_ten_dict = occurrences.most_common(10)
    top_ten_string = top_ten_dict[0][0] + ", " + top_ten_dict[1][0] + ", " + top_ten_dict[2][0] + ", " + \
                     top_ten_dict[3][0] + ", " + top_ten_dict[4][0] + ", " + top_ten_dict[5][0] + ", " + \
                     top_ten_dict[6][0] + ", " + top_ten_dict[7][0] + ", " + top_ten_dict[8][0] + ", " + \
                     top_ten_dict[9][0]
    return top_ten_string


def top_five(list):
    occurrences = Counter(list)
    top_five_dict = occurrences.most_common(5)
    top_five_string = top_five_dict[0][0] + ", " + top_five_dict[1][0] + ", " + top_five_dict[2][0] + ", " + \
                     top_five_dict[3][0] + ", " + top_five_dict[4][0]
    return top_five_string


def top_ten_verbose(list):
    occurrences = Counter(list)
    return occurrences.most_common(10)


def main():
    file = open('honey.log', 'r')
    lines = file.readlines()

    max_failed_root_logins = 0
    current_failed_root_logins = 0

    failed_login_list = []
    failed_ip_list = []
    successful_login_list = []
    passwords_list = []
    unique_source_ips = []
    source_ips_list = []
    command_after_login_list = []

    for i in range(len(lines)):
        line = lines[i]
        line_dict = json.loads(line)

        failed_login_user = get_failed_login_user(line_dict)
        failed_login_ip = get_failed_login_ip(line_dict)
        successful_login_user = get_successful_login_user(line_dict)
        login_attempt_password = get_login_attempt_password(line_dict)
        unique_login_source_ip = get_unique_successful_root_login_ip(line_dict, unique_source_ips)
        source_ip = get_source_ips(line_dict)

        try:
            next_line = lines[i+1]
            next_line_dict = json.loads(next_line)
            command_after_login = get_after_login_command(line_dict, next_line_dict)
            if command_after_login != False:
                command_after_login_list.append(command_after_login)
        except:
            pass
        if failed_login_user != False:
            failed_login_list.append(failed_login_user)
        if failed_login_ip != False:
            failed_ip_list.append(failed_login_ip)
        if successful_login_user != False:
            successful_login_list.append(successful_login_user)
        if login_attempt_password != False:
            passwords_list.append(login_attempt_password)
        if unique_login_source_ip != False:
            unique_source_ips.append(unique_login_source_ip)
        if check_if_root_login_failed(line_dict):
            current_failed_root_logins += 1
            if current_failed_root_logins > max_failed_root_logins:
                max_failed_root_logins = current_failed_root_logins
        else:
            current_failed_root_logins = 0

        source_ips_list.append(source_ip)

    print("Number of failed logins:", len(failed_login_list))
    print("Most common failed login username:", most_frequent(failed_login_list))
    print("Number of successful logins:", len(successful_login_list))
    print("Most common successful login username:", most_frequent(successful_login_list))
    print("Source IP with the most unsuccessful login attempts:", most_frequent(failed_ip_list))
    print("Top ten attempted passwords:", top_ten(passwords_list))
    print("Number of unique source IPs that had a successful root login on first attempt:", len(unique_source_ips))
    print("Max number of failed root logins in a row:", max_failed_root_logins)
    print("Top five commands after login:", top_five(command_after_login_list))

    print("\n\nTop ten source IPs:", top_ten_verbose(source_ips_list))


main()
