import pygame
import mint

def loadChar(hexIn):
    CHAR = []
    index = get_char_index(hexIn)
    for i in range(index, index + 128, 16):
        CHAR.append(Octets[i])

    return CHAR

def hexToInt(var, mode="def"):
    result = int(var, 16) if isinstance(var, str) else var

    if mode == "y":
        result = 15 - result

    return result

def intToHex(value):
    if 0 <= value <= 9:
        return str(value)
    elif value == 10:
        return "A"
    elif value == 11:
        return "B"
    elif value == 12:
        return "C"
    elif value == 13:
        return "D"
    elif value == 14:
        return "E"
    elif value == 15:
        return "F"
    else:
        raise ValueError("Value must be between 1 and 15")

def get_char_index(hex_code):


    x = hexToInt(hex_code[1])
    y = hexToInt(hex_code[2], "y")

    return x + y * 128

def draw_character(character, x, y, PIXEL_SIZE=1):
    for row, line in enumerate(character):
        for col, pixel in enumerate(line):
            if pixel == "1":
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (
                        x + col * PIXEL_SIZE,
                        y + row * PIXEL_SIZE,
                        PIXEL_SIZE,
                        PIXEL_SIZE
                    )
                )

def charToHex(char):
    return octDict.get(char, "x00")

def pgHome():
    screen.fill((0, 0, 0))
        
    global screenX, screenY
    screenX = 0
    screenY = 0  

def render(input_list):
    global screenX, screenY
    for i in input_list:
        draw_character(loadChar(charToHex(i)), screenX, screenY, textSize)
        screenX += 16

def renderln(input_list):
    global screenX, screenY
    screenX = 0
    screenY += 16
    render(input_list)

def renderList(input_list):
    global resHeight
    global resWidth
    fit = int(resHeight/(textSize * 8))
    printingRange = len(input_list) - fit
    index = printingRange
    if(index < 0):
        index = 0
    if(fit > len(input_list)):
        fit = len(input_list)
    for i in range(fit):
        if (i == 0):
            render(str(input_list[index + i]))
        else:
            renderln(str(input_list[index + i]))



def start():
    global screenX
    global screenY
    global character_hex
    global Octets
    global octDict
    global screen
    global resHeight
    global resWidth
    global textSize
    
    textSize = 2
    resHeight = 720
    resWidth = 1280
    screenX = 0
    screenY = 0
    character_hex = "x00"
    Octets = mint.octets # Import character data from mint
    octDict = mint.octetDictionary # Import character dictionary from mint

    # Start pygame and make it look nice.
    pygame.init()
    screen = pygame.display.set_mode((resWidth, resHeight))
    gameIcon = pygame.image.load('D:\\icons\\TangCommandInterfaceIcon.ico')
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("TACOIN")