from blessed import Terminal
from entity import Entity

def render_all(t: Terminal, entities):
    """
    Renders everything. The whole lot.
    """
    for ent in entities:
        render_entity(t, ent)

def render_entity(t: Terminal, ent: Entity):
        print(ent.color(t.move(ent.y, ent.x) + ent.glyph))

# def clear_all(t: Terminal, entities):
#     for ent in entities:
#         clear_entity(t, ent)

# def clear_entity(t: Terminal, ent: Entity):
#     # erase the character that represents this object
#     print(t.move(ent.y, ent.x) + ' ')
