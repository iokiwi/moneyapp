def parse_bool(s):
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    raise ValueError("Cannot parse boolean from {}".format(s))
