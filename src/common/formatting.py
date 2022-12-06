"""_summary_
"""


def format_floats_to_usd(list):
    """_summary_

    Args:
        list (_type_): _description_

    Returns:
        _type_: _description_
    """
    for index, value in enumerate(list):
        if isinstance(value, float):
            list[index] = f"{value:0.2f}$"
    return list
