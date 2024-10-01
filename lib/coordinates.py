def pixel_to_ll(x,y, MAX_Y, MAX_X, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON):
    delta_lat = MAX_LAT-MIN_LAT
    delta_lon = MAX_LON-MIN_LON

    x_frac = float(x)/MAX_X
    y_frac = float(y)/MAX_Y

    lon = MIN_LON + x_frac*delta_lon
    lat = MAX_LAT - y_frac*delta_lat


    calc_x, calc_y = ll_to_pixel(lat, lon, MAX_Y, MAX_X, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON)

    if abs(calc_x-x) > 1 or abs(calc_y-y) > 1:
        print("Mismatch: %s, %s => %s %s" % (
            x,y, calc_x, calc_y))

    return lat, lon

def ll_to_pixel(lat,lon,MAX_Y, MAX_X, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON):
    adj_lat = lat-MIN_LAT
    adj_lon = lon-MIN_LON

    delta_lat = MAX_LAT-MIN_LAT
    delta_lon = MAX_LON-MIN_LON


    lon_frac = adj_lon/delta_lon
    lat_frac = adj_lat/delta_lat

    x = int(lon_frac*MAX_X)
    y = int((1-lat_frac)*MAX_Y)

    return x,y