def get_sector_axis(x, total_sectors, min_value, max_value):
  
  if x < min_value or x > max_value:
    raise ValueError(f"Value {x} is outside the axis range ({min_value}, {max_value})")

  sector_size = (max_value - min_value) / total_sectors

  sector_index = int(x // sector_size) + 1

  return sector_index


def get_combined_sector(x, y, z, total_sectors_per_axis, min_value, max_value):
  
  sector_x = get_sector_axis(x, total_sectors_per_axis, min_value, max_value)
  sector_y = get_sector_axis(y, total_sectors_per_axis, min_value, max_value)
  sector_z = get_sector_axis(z, total_sectors_per_axis, min_value, max_value)
  return (sector_x, sector_y, sector_z)
