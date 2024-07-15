from ursina import *


app = Ursina()

editor_camera = EditorCamera()
editor_camera.speed = 10
editor_camera.rotation_smoothness = 16
editor_camera.fov = 45
editor_camera.fov_smoothness = 16
editor_camera.fov_curve = None
editor_camera.orthographic = False
editor_camera.world_parent = scene

cube = Entity(model='cube', collider='box', scale=2, position=(0, 0, 0), rotation=(0, 0, 0), color=color.azure)


with open('data/athyg_full.csv', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.split(',')
    print(line[16:19])


    

def update():
    pass


app.run()
