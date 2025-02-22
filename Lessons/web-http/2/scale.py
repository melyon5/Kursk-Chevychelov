def get_spn(toponym):
    try:
        envelope = toponym["boundedBy"]["Envelope"]
        lower_corner = envelope["lowerCorner"].split()
        upper_corner = envelope["upperCorner"].split()
        lower_lon, lower_lat = map(float, lower_corner)
        upper_lon, upper_lat = map(float, upper_corner)
        spn_lon = abs(upper_lon - lower_lon)
        spn_lat = abs(upper_lat - lower_lat)
        if spn_lon == 0:
            spn_lon = 0.005
        if spn_lat == 0:
            spn_lat = 0.005
        return f"{spn_lon},{spn_lat}"
    except Exception:
        return "0.005,0.005"
