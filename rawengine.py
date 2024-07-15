from ursina import *

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

app = Ursina()

editor_camera = EditorCamera()
editor_camera.position = (0, 10, 0)
editor_camera.move_speed = 1

stars = []
pointer = Entity(model=Circle(16), color=color.cyan , scale=0.03, position=(0, 0, 0), billboard=True)
pointer.parent = editor_camera




currentregion = (1, 1, 1)
previousregion = (1, 1, 1)
def update():
    global previousregion, currentregion
    previousregion = currentregion
    currentregion = get_combined_sector(editor_camera.position.x*100, editor_camera.position.y*100, editor_camera.position.z*100, 1000, -81000, 33000)
    if currentregion != previousregion:
        print(f"Loading new sector:{currentregion[0]}/{currentregion[1]}/{currentregion[2]}")
        try:
            for star in stars:
                destroy(star)
            stars.clear()

            with open(f'Chunks/Region_{currentregion[0]}_{currentregion[1]}_{currentregion[2]}.csv', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip().split(',')
                    try:
                        stars.append(Entity(model=Circle(5), billboard=True, scale=0.01, position=(float(line[16])/100, float(line[17])/100, float(line[18])/100)))
                        #print((float(line[16])/100, float(line[17])/100, float(line[18])/100))
                    except:
                        pass
        except:
           pass

    #print(currentregion)


app.run()
