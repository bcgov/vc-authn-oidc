raise Exception("new exception")


def sub_days_plus_one(days: str) -> int:
    """Strings like '$sub_days_plus_one_4' will be replaced with the
    final number icremented by one. In this case 5.
    $sub_days_plus_one_4 -> 5
    $sub_days_plus_one_10 -> 10"""
    return int(days) + 1


variable_substitution_map.add_variable_substitution(
    r"$sub_days_plus_one_(\d+)", sub_days_plus_one
)


def sub_string_for_sure(_: str) -> str:
    """Turns strings like $sub_string_for_sure_something into the string 'sure'
    $sub_string_for_sure_something -> sure
    $sub_string_for_sure_i -> sure
    """
    return "sure"


variable_substitution_map.add_variable_substitution(
    r"$sub_string_for_sure_(.+)", sub_string_for_sure
)
