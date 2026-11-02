import pygame
import mint

# Tacoin! The world's most advanced terminal interface. Ever. I promise.
# Module made by MinFou for the Tang project, and possibly other things.

def loadChar(hexIn): # Creates a matrix for the character rendering
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

def draw_character(character, x, y, PIXEL_SIZE=1, rgb = [0, 255, 0], draw_black = False):
    for row, line in enumerate(character):
        for col, pixel in enumerate(line):
            if pixel == "1":
                pygame.draw.rect(
                    screen,
                    (rgb[0], rgb[1], rgb[2]),
                    (
                        x + col * PIXEL_SIZE,
                        y + row * PIXEL_SIZE,
                        PIXEL_SIZE,
                        PIXEL_SIZE
                    )
                )
            elif (draw_black):
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
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

def render(input_list, x = None, y = None, drawBlack = False):
    global screenX, screenY
    if(x == None):
        x = screenX
    if(y == None):
        y = screenY
    CULL_CHARS = {"x00", "x02"}             # We don't like these ones because they hold no actual data, just zeros. These are the NULL and space characters.

    for i in input_list:
        char_hex = charToHex(i)

        if char_hex not in CULL_CHARS:
            draw_character(loadChar(char_hex), x, y, textSize, draw_black = drawBlack)
        x += 16

    screenX = x

def renderln(input_list, draw_black = False): # Render and then start a new line
    global screenX, screenY
    screenX = 0
    screenY += 16
    render(input_list, drawBlack = draw_black)

def renderList(input_list, scroll=0):
    """Render a scrollable list of text lines."""

    global resHeight, resWidth

    if not input_list:
        return

    line_height = 16

    fit = max(1, resHeight // line_height)

    # Clamp scroll to the valid range.
    max_scroll = max(0, len(input_list) - fit)
    scroll = max(0, min(int(scroll), max_scroll))

    # Calculate the visible range.
    start_index = max_scroll - scroll
    end_index = min(start_index + fit, len(input_list))

    # Reset cursor before drawing.
    global screenX, screenY

    screenX = 0
    screenY = 0

    for index in range(start_index, end_index):

        if index == start_index:
            render(str(input_list[index]))
        else:
            renderln(str(input_list[index]))
    return scroll

def start():
    # I like making it look like this.
    # Don't judge me!!!
    global screenX
    global screenY
    global character_hex
    global Octets
    global octDict
    global screen
    global resHeight
    global resWidth
    global textSize
    
    textSize = 2 # How big a pixel is
    resHeight = 720 # How tall window
    resWidth = 1280 # How wide window
    screenY = 0 # Where the next line of text is being placed
    screenX = 0 # Where the characters go on that line
    character_hex = "x00" # Just set to NULL so nothing gets printed on accident
    Octets = mint.octets # Import character data from mint
    octDict = mint.octetDictionary # Import character dictionary from mint

    # Start pygame and make it look nice.
    pygame.init() # Open terminal window
    screen = pygame.display.set_mode((resWidth, resHeight)) # Black magic
    gameIcon = pygame.image.load('Assets\\TangCommandInterfaceIcon.ico') # I drew this myself
    pygame.display.set_icon(gameIcon) 
    pygame.display.set_caption("TACOIN") # This is what it's called