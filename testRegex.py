import re


def test_string_list(string_list, regex_string):
    result = []
    regex = re.compile(regex_string)
    for should_accept in string_list:
        match = regex.match(should_accept)
        result.append("{}{}".format("<font color = green >ACCEPT: " if match else "<font color = red>REJECT: ",
                                    should_accept.replace('$','\$') + "</font>"))
    return "<br/>".join(result)


def test_regex(should_accept=None, should_reject=None, user_test_string=None, regex=""):
    regex = "^" + regex + "$"
    result = "<h2>Test Strings:</h2>\n"
    result += test_string_list(user_test_string, regex)
    if should_accept:
        result += "\n<h2>Test Suite: (Should be ACCEPTED)</h2>\n"
        result += test_string_list(should_accept, regex)
    if should_reject:
        result += "\n<h2>Test Suite: (Should be REJECTED)</h2>\n"
        result += test_string_list(should_reject, regex)
    return result
