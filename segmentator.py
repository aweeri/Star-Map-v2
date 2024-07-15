import csv
import os


filecount = 0
for file in os.listdir('Chunks'):
    os.remove(os.path.join('Chunks', file))
    filecount += 1
print(f"Purged {filecount} files")


chunkcount = 1000


bounds = {
    'minx': -24565.642,
    'maxx': 23668.645,

    'miny': -58307.612,
    'maxy': 32956.151,

    'minz': -80933.773,
    'maxz': 28759.517
}



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


with open('data/athyg_full.csv', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(',')
        try:
            print(f"{round((float(line[0])/2500000)*100, 2)}%")
        except:
           pass
        try:
            region = get_combined_sector(float(line[16]), float(line[17]), float(line[18]), chunkcount, -81000, 33000)
            file = open(f'Chunks/Region_{region[0]}_{region[1]}_{region[2]}.csv', 'a', newline='')
            writer = csv.writer(file)
            writer.writerow(line)
        except:
            pass

