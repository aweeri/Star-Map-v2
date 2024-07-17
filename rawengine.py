from ursina import *
import threading
import csv
import time

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
editor_camera.move_speed = 5

grid = Entity(model=Grid(128,128), scale=48, position=(0, 0, 0),rotation=(90, 0, 0), color=color.gray)

stars = []
pointer = Entity(model=Circle(16), color=color.cyan , scale=0.03, position=(0, 0, 0), billboard=True)
pointer.parent = editor_camera

def renderChunk(lines):
    for line in lines:
        line = line.strip().split(',')
        try:
            floats = [float(line[i]) / 100 for i in range(16, 19)]
            stars.append(Entity(model=Circle(5), billboard=True, scale=0.01, position=floats))
        except:
            pass

threadStop = False

def readChunk(rX,rY,rZ):
    global threadStop
    with open(f'Chunks/Region_{rX}_{rY}_{rZ}.csv', 'r') as file:
                lines = file.readlines()
                length = len(lines)
                print(length)
                
                

                if len(lines) > 200:
                    half = len(lines) // 2
                    first_half = lines[:half]
                    second_half = lines[half:]

                    renderThread1 = threading.Thread(target=renderChunk, args=([first_half]))
                    renderThread2 = threading.Thread(target=renderChunk, args=([second_half]))
                    renderThread1.start()
                    renderThread2.start()
                
                
                
                else:
                    renderChunk(lines)




chunkwidth = 0

with open('Chunks/seginfo.dat', 'r') as segfile:
    chunkwidth = int(segfile.read())
    print(f"chunkwidth is {chunkwidth}")

currentregion = (1, 1, 1)
previousregion = (1, 1, 1)
def update():

    if held_keys["escape"]:
        quit()

    global previousregion, currentregion, threadStop
    
    previousregion = currentregion
    currentregion = get_combined_sector(editor_camera.position.x*100, editor_camera.position.y*100, editor_camera.position.z*100, chunkwidth, -81000, 33000)
    if currentregion != previousregion:
        
        print(f"Loading new sector:{currentregion[0]}/{currentregion[1]}/{currentregion[2]}")
        try:
            for star in stars:
                destroy(star)
            stars.clear()

            #split_and_process(currentregion[0],currentregion[1],currentregion[2], 2)
            loadingThread = threading.Thread(target=readChunk, args=(currentregion[0],currentregion[1],currentregion[2]))
            loadingThread.start()
            
        except:
           pass
    #print(currentregion)


app.run()
