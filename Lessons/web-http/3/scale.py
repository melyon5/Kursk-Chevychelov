def get_spn_points(coord1, coord2, factor=1.3, default=0.005):
    lon1, lat1 = map(float, coord1.split(","))
    lon2, lat2 = map(float, coord2.split(","))
    spn_lon = abs(lon1 - lon2) * factor
    spn_lat = abs(lat1 - lat2) * factor
    if spn_lon < default:
        spn_lon = default
    if spn_lat < default:
        spn_lat = default
    return f"{spn_lon},{spn_lat}"
