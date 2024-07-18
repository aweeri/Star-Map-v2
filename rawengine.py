from ursina import *
import threading
import csv
import time
from modules import lookup

app = Ursina()



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



editor_camera = EditorCamera()
editor_camera.position = (30, 2, 2)
editor_camera.move_speed = 2
text = Text(position=(-.2, .2), scale=0.1)

grid = Entity(model=Grid(128,128), scale=128, position=(0, 0, 0),rotation=(90, 0, 0), color=color.rgba(1, 1, 1, 0.05))

hoverSel = None
worldScale = 10 # higher values shrink the world down

class Star(Entity):
    def __init__(self, coords=(0, 0, 0), inx = -1, absmag = 0):
        super().__init__(
            model=Circle(5),
            billboard=True,
            scale = (-0.003*float(absmag)),
            position=coords,
            collider='mesh'
            )
        self.inx = inx
    def update(self):
        global hoverSel
        if mouse.hovered_entity:
            text.text = f"{lookup.starLookup('data/athyg_full.csv', self.inx)}"
        else:
            text.text = ""


        
                


stars = []
pointer = Entity(model=Circle(16), color=color.cyan , scale=0.03, position=(0, 0, 0), billboard=True)
pointer.parent = editor_camera

def renderChunk(lines):
    global worldScale
    try:
        lines = [line.strip().split(',') for line in lines]
        lines = [[float(line[0])/worldScale, float(line[1])/worldScale, float(line[2])/worldScale] + line[3:] for line in lines]
        stars = [Star(coords, line[0], float(line[4])) for line in lines]
    except:
        pass

threadStop = False

def readChunk(rX,rY,rZ):
    global threadStop
    with open(f'Chunks/Region_{rX}_{rY}_{rZ}.csv', 'r') as file:
                lines = file.readlines()
                length = len(lines)
                #print(length)

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
    global hoverSel
    #print(threading.enumerate())
    if held_keys["escape"]:
        quit()

    global previousregion, currentregion, threadStop, worldScale
    
    previousregion = currentregion
    currentregion = get_combined_sector(editor_camera.position.x*worldScale, editor_camera.position.y*worldScale, editor_camera.position.z*worldScale, chunkwidth, -81000, 33000)
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
