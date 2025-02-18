def get_spn(geo_obj) -> tuple[str, str]:
    env = geo_obj['boundedBy']['Envelope']
    lower = list(map(float, env['lowerCorner'].split()))
    upper = list(map(float, env['upperCorner'].split()))
    span_lon = str(abs(upper[0] - lower[0]))
    span_lat = str(abs(upper[1] - lower[1]))
    return span_lon, span_lat