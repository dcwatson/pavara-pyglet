def parse_int(s, default=0):
    if s is None or not s.strip():
        return default
    return int(s.strip())

def parse_float(s, default=0.0):
    if s is None or not s.strip():
        return default
    return float(s.strip())

def parse_bool(s, default=False):
    if s is None or not s.strip():
        return default
    return s.strip().lower() in ('yes', 'y', 'true', 't', '1')

def parse_vector(s, default=None):
    if s is None or not s.strip():
        return default or (0, 0, 0)
    return [float(v.strip()) for v in s.split(',')]

def parse_color(s, default=None):
    v = parse_vector(s, default)
    if len(v) == 3:
        return list(v) + [1]
    return v
