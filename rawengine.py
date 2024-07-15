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
lista = []
for line in lines:
    line = line.split(',')
    
    try:
        line[16:19] = [float(num) for num in line[16:19]]
        lista.append(line[16:19])
    except:
        pass
print(lista[0:5])



    

def update():
    pass


app.run()
