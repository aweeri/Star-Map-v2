from ursina import Ursina, Entity, mouse

app = Ursina()

box = Entity(model="cube", texture="white", collider="box")  # Create a white box

def on_hover():
    if mouse.hovered_entity == box:
        print("x")

box.on_mouse_enter = on_hover  # Call the function when hovering over the box

app.run()