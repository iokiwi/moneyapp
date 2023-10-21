def parse_bool(s):
    if type(s) is bool:
        return s

    if type(s) is not str:
        raise ValueError("value is not string")

    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False

    raise ValueError(str(s))
