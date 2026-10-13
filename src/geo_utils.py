import math

EARTH_RADIUS = 6378137.0

def pixel_to_geo(px, py, drone_lat, drone_lon, drone_alt,
                 gimbal_pitch_deg, gimbal_yaw_deg,
                 hfov_deg, vfov_deg, img_w, img_h):
    """Грубая проекция пикселя на землю (flat earth для малых углов)."""
    dx = (px - img_w / 2) / (img_w / 2)
    dy = (py - img_h / 2) / (img_h / 2)
    yaw = math.radians(gimbal_yaw_deg)
    pitch = math.radians(gimbal_pitch_deg)
    slant_range = drone_alt / max(math.sin(-pitch), 1e-3)
    ground_range = slant_range * math.cos(pitch)
    x_off = ground_range * math.tan(math.radians(hfov_deg / 2)) * dx
    y_off = ground_range * math.tan(math.radians(vfov_deg / 2)) * dy
    east = x_off * math.cos(yaw) - y_off * math.sin(yaw)
    north = x_off * math.sin(yaw) + y_off * math.cos(yaw)
    dlat = north / EARTH_RADIUS * 180 / math.pi
    dlon = east / (EARTH_RADIUS * math.cos(math.radians(drone_lat))) * 180 / math.pi
    return drone_lat + dlat, drone_lon + dlon
