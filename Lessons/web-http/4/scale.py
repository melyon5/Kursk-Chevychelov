def get_map_params(coordinates, margin=0.1, default=0.005):
    lons = [float(coord.split(",")[0]) for coord in coordinates]
    lats = [float(coord.split(",")[1]) for coord in coordinates]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    spn_lon = (max_lon - min_lon) * (1 + margin)
    spn_lat = (max_lat - min_lat) * (1 + margin)
    if spn_lon < default:
        spn_lon = default
    if spn_lat < default:
        spn_lat = default
    center = f"{center_lon},{center_lat}"
    spn = f"{spn_lon},{spn_lat}"
    return center, spn
