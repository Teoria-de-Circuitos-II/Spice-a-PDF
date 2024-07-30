import svgwrite
import re
import os
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

font_path = os.path.join('fonts', 'cmunrm.ttf')


class Component:
    def __init__(slf, component_type, position, orientation, flip, attributes, windows):
        slf.component_type = component_type
        slf.position = position
        slf.orientation = orientation
        slf.flip = flip
        slf.attributes = attributes
        slf.windows = windows

    def draw(slf, dwg):
        raise NotImplementedError

    def adjust_coordinates_for_orientation_and_alignment(slf, x, y, alignment):
        if alignment == "Left":
            if slf.orientation == "R0":
                y += 6.5
                return x, y
            elif slf.orientation == "R90":
                x += 7
                return -y, x
        elif alignment == "VTop":
            if slf.orientation == "R90":
                x += 22
            elif slf.orientation == "R270":
                x += 6
        elif alignment == "VBottom":
            if slf.orientation == "R90":
                x -= 6
            elif slf.orientation == "R270":
                x -= 18

        return slf.rotate_coordinates(x, y)

    def rotate_coordinates(slf, x, y):
        if slf.orientation == "R0":
            return x, y
        elif slf.orientation == "R90":
            return -y, x
        elif slf.orientation == "R180":
            return -x, -y
        elif slf.orientation == "R270":
            return y, -x
                

    def add_text(slf, dwg, x, y, window, text, size = "20px", angle = 0):
        if(not(x == 25040.2 and y == -25040.2)):
            coords = slf.adjust_coordinates_for_orientation_and_alignment(window[0], window[1], window[2])
            if coords is None:
                raise ValueError("Coords cannot be None. Please check the window value.")
            
            if window[2] in ["VTop", "VBottom"]:
                dwg.add(dwg.text(text, insert=(x + (slf.flip) * coords[0], y + coords[1]), font_family="CMU Serif", font_size=size, text_anchor="middle"))
            else:
                text_element = dwg.text(text, insert=(x + ((slf.flip) * coords[0]), y + coords[1]), font_family="CMU Serif", font_size=size, text_anchor="end" if (((slf.orientation == "R90" or slf.orientation == "R180") and slf.flip == 1) or ((slf.orientation == "R0" or slf.orientation == "R270") and slf.flip == -1)) else "start")
                text_element.rotate(-angle, center = (x + coords[0], y + coords[1]))
                dwg.add(text_element)

    def draw_image_with_rotation(slf, dwg, href):
        x, y = slf.position
        image = svgwrite.image.Image(href=href, insert=(x, y))

        if slf.flip == -1:
            # Espejado
            angle = int(slf.orientation[1:])
            transform = f"scale(-1, 1) translate({-2 * x}, 0) rotate({angle}, {x}, {y})"
        else:
            # Rotación normal
            angle = int(slf.orientation[1:])
            transform = f"rotate({angle}, {x}, {y})"
        
        image['transform'] = transform
        dwg.add(image)





class Amp_Current(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/Amp_Current.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Amp_Transimpedance(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/Amp_Transimpedance.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Ampmeter(Component):
    def draw(slf, dwg): 
        slf.draw_image_with_rotation(dwg, 'Skins/Default/ampmeter.svg')
        offset = offset_text(slf, 7, 0, -2, 0)

        slf.add_text(dwg, slf.position[0] + offset, slf.position[1] + offset, slf.windows.get(0, (-23, 14, "Left")), slf.attributes.get("InstName", ""), angle = 90)

class Arrow(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/arrow.svg')
        offsetx = offset_text(slf, 0, 3, 0, 11)
        offsety = offset_text(slf, 2, 0, 0, 2)
        slf.add_text(dwg, slf.position[0] + offsetx, slf.position[1] + offsety, slf.windows.get(3, (21, -18, "Left")), slf.attributes.get("Value", "Ir"), angle = (int(slf.orientation[1:]))%180)

class Arrow_curve(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/arrow_curve.svg')
        offsetx = offset_text(slf, 3, 7, -3, -9)
        offsety = offset_text(slf, -1, 15, -7, -4)
        slf.add_text(dwg, slf.position[0] + offsetx, slf.position[1] + offsety, slf.windows.get(3, (63, 55, "Left")), slf.attributes.get("Value", "Vr"))

class Bi(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/bi.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Bv(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/bv.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Bypass(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/bypass.svg')

class Capacitor(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/cap.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1] - 8, slf.windows.get(0, (24, 8, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1] + 5, slf.windows.get(3, (24, 56, "Left")), slf.attributes.get("Value", slf.component_type))

class Cell(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/cell.svg')
        slf.add_text(dwg, slf.position[0] - 12, slf.position[1] + 6, slf.windows.get(0, (24, 8, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0] - 12, slf.position[1] - 8, slf.windows.get(3, (24, 56, "Left")), slf.attributes.get("Value", slf.component_type))

class Current(Component):
    def draw(slf, dwg):

        offset = offset_text(slf, 15, 0, 15, 0)
    
        slf.draw_image_with_rotation(dwg, 'Skins/Default/current.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1] - offset - 3, slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1] - offset, slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type))

class Diode(Component):
    def draw(slf, dwg):
        offsety = offset_text(slf, 0, 0, 0, 3)
        slf.draw_image_with_rotation(dwg, 'Skins/Default/diode.svg')
        slf.add_text(dwg, slf.position[0] + 1, slf.position[1] + 3, slf.windows.get(0, (24, 0, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0] + 3, slf.position[1] - 4 + offsety, slf.windows.get(3, (24, 64, "Left")), slf.attributes.get("Value", slf.component_type))

class E(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/e.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class E2(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/e2.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Flag(Component):
    def draw(slf, dwg):
        if(slf.attributes.get("Value", slf.component_type) == "0"):

            direction = get_cable_directions(slf.position, wires)
            if direction == "up":
                slf.orientation = "R0"
            elif direction == "down":
                slf.orientation = "R180"
            elif direction == "left":
                slf.orientation = "R270"
            elif direction == "right":
                slf.orientation = "R90"

            slf.draw_image_with_rotation(dwg, 'Skins/Default/GND.svg')
        else:
            slf.draw_image_with_rotation(dwg, 'Skins/Default/FLAG.svg')
            place_text_according_to_cable(slf.position, slf.attributes.get("Value", slf.component_type), wires, dwg)

class G(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/g.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class G2(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/g2.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Inductor(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/ind.svg')
        offsetx = offset_text(slf, 0, 0, -40)
        slf.add_text(dwg, slf.position[0] + offsetx, slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0] + offsetx, slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type))

class LTap(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/L_Tap.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (40, 58, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(123, (40, 134, "Left")), slf.attributes.get("Value2", "n=3"), angle = (int(slf.orientation[1:]))%180)

class LM311(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/LM311.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (-112, -16, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (-112, 7, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(69, (-89, 82, "Left")),slf.attributes.get("Value", "O_GND"), "8px", angle = (int(slf.orientation[1:]))%180)

class NJFet(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/njf.svg')
        offsetx = offset_text(slf, -25, -41, -63, -35)
        offsety = offset_text(slf, 10, 34, 51, 40)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class NMOS(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/nmos.svg')
        offsetx = offset_text(slf, -30, -41, -63, -35)
        offsety = offset_text(slf, 20, 34, 51, 40)
        slf.add_text(dwg, slf.position[0] + offsety, slf.position[1] + offsetx, slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class NPN(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/npn.svg')
        offsetx = offset_text(slf, -30, -41, -63, -35)
        offsety = offset_text(slf, 20, 34, 51, 40)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class Not(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/74HCU04 Not.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (16, 16, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (7, 87, "Left")), slf.attributes.get("Value", "74HCU04"), "11px",  (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(69, (7, 28, "Left")), slf.attributes.get("Value", "Vdd"), "10px",  (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(125, (7, 104, "Left")), slf.attributes.get("Value2", "GND"), "10px", (int(slf.orientation[1:]))%180)

class OpAmp(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/OA_Ideal.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (24, 8, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (-176, 32, "Left")), slf.attributes.get("Value", slf.component_type), "9px",  (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(123, (-176, 48, "Left")), slf.attributes.get("Value2", slf.component_type), "9px", (int(slf.orientation[1:]))%180)

class PJFet(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/pjf.svg')
        offsetx = offset_text(slf, -30, -41, -63, -35)
        offsety = offset_text(slf, 20, 34, 51, 40)
        slf.add_text(dwg, slf.position[0] + offsety, slf.position[1] + offsetx, slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class PMOS(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/pmos.svg')
        offsetx = offset_text(slf, -30, -41, -63, -35)
        offsety = offset_text(slf, 20, 34, 51, 40)
        slf.add_text(dwg, slf.position[0] + offsety, slf.position[1] + offsetx, slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class PNP(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/PNP.svg')
        offsetx = offset_text(slf, -30, -41, -63, -35)
        offsety = offset_text(slf, 20, 34, 51, 40)
        slf.add_text(dwg, slf.position[0] + offsety, slf.position[1] + offsetx, slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))

class Pot(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/pot.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type))

class Resistor(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/ress.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type))

class Res60(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/res_60.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type), angle = (int(slf.orientation[1:]))%180)

class Schottky(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/schottky.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1] - 8, slf.windows.get(0, (56, 32, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1] + 5, slf.windows.get(3, (56, 68, "Left")), slf.attributes.get("Value", " "))

class Switch(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/switch.svg')        

class SwitchSch(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/switch_sch.svg')
        
class TL082(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/TL082.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (24, 8, "Left")), slf.attributes.get("InstName", ""), angle = (int(slf.orientation[1:]))%180)

class Voltage(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/voltage.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (36, 40, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (36, 76, "Left")), slf.attributes.get("Value", slf.component_type))

class Zener(Component):
    def draw(slf, dwg):
        slf.draw_image_with_rotation(dwg, 'Skins/Default/zener.svg')
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(0, (24, 0, "Left")), slf.attributes.get("InstName", ""))
        slf.add_text(dwg, slf.position[0], slf.position[1], slf.windows.get(3, (24, 64, "Left")), slf.attributes.get("Value", slf.component_type))

def offset_text (slf, off0 = 0, off90  = 0, off180  = 0, off270  = 0):
    if (slf.orientation == "R0"):
        return  off0
    elif(slf.orientation == "R90"):
        return off90
    elif(slf.orientation == "R180"):
        return off180
    elif(slf.orientation == "R270"):
        return off270
    else:
        return 0


def parse_asc_file(filename):
    wires = []
    components = []
    current_component = None
    windowsize = None

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == "WIRE":
                x1, y1, x2, y2 = map(int, parts[1:])
                wires.append(((x1, y1), (x2, y2)))
            elif parts[0] == "SYMBOL":
                if current_component:
                    components.append(current_component)
                component_type = parts[1]
                if '\\' in component_type:
                    component_type_parts = component_type.split('\\')
                    # Caso especial: si el nombre del componente termina en "\\"
                    if component_type_parts[-1] == '':
                        component_name = parts[2]
                        coords_and_orientation = parts[3:]
                    else:
                        component_name = component_type_parts[-1].split()[-1]
                        coords_and_orientation = parts[2:]
                else:
                    component_name = component_type
                    coords_and_orientation = parts[2:]

                x, y = map(int, coords_and_orientation[:2])
                orientation = coords_and_orientation[2] if len(coords_and_orientation) > 2 else "R0"

                if orientation.startswith("M"):
                    orientation = 'R' + orientation[1:]
                    flip = -1
                else:
                    flip = 1
                
                current_component = {"type": component_name, "position": (x, y), "orientation": orientation, "flip": flip, "attributes": {}, "windows": {}}
            elif parts[0] == "SYMATTR" and current_component:
                attribute_name = parts[1]
                attribute_value = " ".join(parts[2:])
                current_component["attributes"][attribute_name] = attribute_value
            elif parts[0] == "WINDOW" and current_component:
                if "Invisible" in parts:
                    x = 25040.2
                    y = -25040.2
                else:
                    x, y = map(int, parts[2:4])

                window_index = int(parts[1])
                alignment = parts[4]
                current_component["windows"][window_index] = (x, y, alignment)
            elif parts[0] == "FLAG":
                x, y = map(int, parts[1:3])
                component_type = "flag"
                orientation = "R0"
                flip = 1
                flag = {"type": component_type, "position": (x, y), "orientation": orientation, "flip": flip,"attributes": {}, "windows": {}}
                flag["attributes"]["Value"] = parts[3]
                components.append(flag)
            elif parts[0] == 'SHEET':
                windowsize = (parts[2], parts[3])

        if current_component:
            components.append(current_component)

    return wires, components, windowsize

def get_cable_directions(pin_position, cables):
    directions = []
    for (start, end) in cables:
        if pin_position == start:
            dx = end[0] - start[0]
            dy = end[1] - start[1]
        elif pin_position == end:
            dx = start[0] - end[0]
            dy = start[1] - end[1]
        else:
            continue
        
        if dx > 0 and "right" not in directions:
            directions.append("right")
        elif dx < 0 and "left" not in directions:
            directions.append("left")
        if dy > 0 and "down" not in directions:
            directions.append("down")
        elif dy < 0 and "up" not in directions:
            directions.append("up")
    
    if directions:
        return ", ".join(directions)
    else:
        return None

def place_text_according_to_cable(pin_position, text, cables, dwg, offset=20):
    directions = get_cable_directions(pin_position, cables)
    
    if "up" in directions:
        if "right" in directions:
            text_position = (pin_position[0] - int(offset/2), pin_position[1] + 5)
            dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="end"))
        else:
            text_position = (pin_position[0], pin_position[1] + offset)
            dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="middle"))

    elif "down" in directions:
        text_position = (pin_position[0], pin_position[1] - offset + 10)
        dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="middle"))

    elif "left" in directions:
        if "right" in directions:
            text_position = (pin_position[0], pin_position[1] - offset + 10)
            dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="middle"))
        else:
            text_position = (pin_position[0] + int(offset/2), pin_position[1] + 5)
            dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="start"))

    elif "right" in directions:
        text_position = (pin_position[0] - int(offset/2), pin_position[1] + 5)
        dwg.add(dwg.text(text, insert=text_position, font_family="CMU Serif", font_size="20px", text_anchor="end"))

    else:
        text_position = pin_position
    
    
def create_circuit_svg(filename, wires, components):
    dwg = svgwrite.Drawing(filename, size=windowsize, profile='tiny')
    nodes = {}

    # Dibujar cables y detectar nodos
    for (start, end) in wires:
        dwg.add(dwg.line(start=start, end=end, stroke=svgwrite.rgb(0, 0, 0, '%'), stroke_width=1.5))
        for point in [start, end]:
            if point in nodes:
                nodes[point] += 1
            else:
                nodes[point] = 1

    # Dibujar nodos si se intersectan 3 o más cables
    for point, count in nodes.items():
        if count >= 3:
            dwg.add(dwg.circle(center=point, r=4, fill='black'))

    # Dibujar componentes
    component_objects = {
        "Not": Not,     
        "Amp_Current": Amp_Current,
        "Amp_Transimpedance": Amp_Transimpedance,
        "ampmeter": Ampmeter, 
        "arrow": Arrow,
        "arrow_curve": Arrow_curve,
        "bv": Bv,
        "bi": Bi,
        "bypass": Bypass,
        "current": Current,
        "cell": Cell,
        "diode": Diode,
        "e": E,
        "e2": E2,
        "g": G,
        "g2": G2,
        "L_Tap": LTap,
        "LM311": LM311,
        "njf": NJFet,
        "nmos": NMOS,
        "pjf": PJFet,
        "pmos": PMOS,
        "res_60": Res60,
        "schottky": Schottky,
        "switch": Switch,
        "switch_sch": SwitchSch,
        "zener": Zener,
        "res": Resistor,
        "cap": Capacitor,
        "OA_Ideal": OpAmp,
        "flag": Flag,
        "npn": NPN,
        "pnp": PNP,
        "ind": Inductor,
        "pot": Pot,
        "TL082": TL082,
        "voltage": Voltage
    }

    for component in components:
        component_type = component["type"]
        if component_type in component_objects:
            component_obj = component_objects[component_type](
                component_type,
                component["position"],
                component["orientation"],
                component["flip"],
                component["attributes"],
                component["windows"]
            )
            component_obj.draw(dwg)

    dwg.save()

def modify_svg_font(svg_filename, output_svg_filename, font_name):
    with open(svg_filename, 'r', encoding='utf-8') as file:
        svg_content = file.read()
    
    # Reemplaza cualquier referencia de fuente por CMU Serif
    modified_svg_content = re.sub(r'font-family="[^"]+"', f'font-family="{font_name}"', svg_content)
    
    with open(output_svg_filename, 'w', encoding='utf-8') as file:
        file.write(modified_svg_content)

def svg_to_pdf(svg_filename, pdf_filename):
    # Registrar la fuente CMU Serif
    pdfmetrics.registerFont(TTFont('CMU_Serif', font_path))
    
    # Registrar la fuente con el mapeo de svglib
    from svglib.fonts import register_font
    register_font('CMU_Serif', font_path)
    
    # Leer el dibujo SVG
    drawing = svg2rlg(svg_filename)
    
    # Crear el canvas PDF
    c = canvas.Canvas(pdf_filename, pagesize= windowsize)
    
    # Dibujar el SVG en el PDF
    renderPDF.draw(drawing, c, 0, 0)
    
    # Guardar el PDF
    c.showPage()
    c.save()


# Ejemplo de uso
asc_filename = 'Guia1.asc'
modified_svg_filename = 'ModifiedOutput.svg'
svg_filename = 'Output.svg'
pdf_filename = 'Output.pdf'

wires, components, windowsize = parse_asc_file(asc_filename)

create_circuit_svg(svg_filename, wires, components)

# Modifica el SVG para usar CMU Serif
modify_svg_font(svg_filename, modified_svg_filename, 'CMU_Serif')

svg_to_pdf(modified_svg_filename, pdf_filename)
