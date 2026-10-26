import sys
import json
import tacoin
import mint
import pygame

mint.PLACEHOLDER() # Just keep mint in mind (Super placeholder)
#Definitions

def SystemStart():
    # Init globals
    global PTIMB
    global PTIMB_Size
    global maxByteAmount
    global running
    global talkbox
    global byteSize
    global PTIMB_AvaiableAddress
    global processPTIMBaddress
    global Display
    global processPointer

    processPTIMBaddress = 1
    PTIMB_AvaiableAddress = 0
    byteSize = 16
    Display = []
    maxByteAmount = toInt("1"*byteSize, "string") # Decides how long PTIMB should be
    PTIMB_Size = maxByteAmount
    PTIMB = bytearray(PTIMB_Size) # Thus it begins
    running = True
    talkbox = ""
    processPointer = 0
    
def breakpoint(msg: str, mode: str = "non-fatal"):
    if mode == "fatal":
        print(f"FATAL BREAKPOINT: {msg}")
        sys.exit()
    else:
        print(f"BREAKPOINT: {msg}")
        running = False
             
def toString(number: int) -> str:

    # Mostly obsolete
    #Converts an integer between 0 and 255 into an 8-bit binary string.  
    if not (0 <= number <= maxByteAmount):
        raise ValueError(f"Number must be between 0 and {maxByteAmount} for an 8-bit byte.")
        
    return f"{number:0{byteSize}b}"

def endTang():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
def toInt(bit_string, mode = "pass"):
    #Turns an 8-bit binary string into an integer.
    # Mostly obsolete
    if(mode == "string"):
        if(type(bit_string) == str):
            if(len(bit_string) != byteSize):
                raise ValueError(f"The input string must be exactly {byteSize} bits long.\n     The provided input is {len(bit_string)} bits long. ({bit_string})")
        else:
            raise ValueError("toInt requires a bit string as input.")

        return int(bit_string, 2)
    elif(mode == "pass"):
        return bit_string

def newData(index, length): # Primitive for making a new array
    if(PTIMB[index] != 0):
        raise ValueError("PTIMB space is occupied")
    PTIMB[index] = length + index + 2 # Place start cap
    PTIMB[index + 1] = 0 # Initialize the data pointer
    PTIMB[index + length + 2] = index # Place end cap
    PTIMB[PTIMB_AvaiableAddress] = index + length + 3 # Update the available address

def insertItem(indexOfData, atPos, inject): #The index of the Array, what you are injecting, and where in the array you want it to go.
    if(PTIMB[PTIMB[indexOfData]] != indexOfData):
        raise ValueError("Selected PTIMB is not closed.")
    if(PTIMB[indexOfData] <= atPos + indexOfData):
        raise ValueError("PTIMB is not long enough to contain data at specified index.")
    PTIMB[indexOfData + 2 + atPos] = inject
    if(PTIMB[indexOfData + 2 + atPos] != inject):
        raise ValueError("Failed to insert item.")

def addItem(index: int, add: int): #Streamlined method for adding to a PTIMB array.
    insertItem(index, PTIMB[index + 1], add)
    #print(f"DEBUG: Added {add} to stack at address {index + 1}")
    indexPointer = toInt(PTIMB[index + 1]) + 1
    PTIMB[index+1] = indexPointer

def getIndex(sourceIndex: int, itemIndex: int) -> str:
    if not isinstance(sourceIndex, int) or not isinstance(itemIndex, int):
        raise TypeError("sourceIndex and itemIndex must be integers.")

    targetIndex = sourceIndex + 2 + itemIndex
    if targetIndex < 0 or targetIndex >= len(PTIMB):
        raise IndexError(
            f"Requested PTIMB item index {targetIndex} is outside the valid range "
            f"0..{len(PTIMB) - 1}."
        )

    result = targetIndex
    
    return result
    
def getItem(sourceIndex: int, itemIndex: int) -> str:
    """Return a binary byte stored in a PTIMB data block.

    PTIMB entries are arranged as:
      [0] length/metadata
      [1:] data bytes
    This helper resolves the item offset relative to a data block and validates
    that the target is a valid byte-sized binary string.
    """
    if not isinstance(sourceIndex, int) or not isinstance(itemIndex, int):
        raise TypeError("sourceIndex and itemIndex must be integers.")

    targetIndex = sourceIndex + 2 + itemIndex
    if targetIndex < 0 or targetIndex >= len(PTIMB):
        raise IndexError(
            f"Requested PTIMB item index {targetIndex} is outside the valid range "
            f"0..{len(PTIMB) - 1}."
        )

    result1 = PTIMB[targetIndex]
    if (type(result1) != int):
        printRAM(0,100)
        raise ValueError(f"Memory has been dummped;\nPTIMB entry at index {targetIndex} is not a bit integer: {result1!r}")

    return result1

def getArrLen(address: int):
    if(PTIMB[address] != 0): #Check if address is empty
            if(PTIMB[PTIMB[address]] == address): #Check if address is a closed loop
                return PTIMB[address + 1]
            else:
                breakpoint("Cannot identify a non-existent array","fatal")

def getArray(address: int):
    construct = []
    if(PTIMB[address] != 0): #Check if address is empty
            if(PTIMB[PTIMB[address]] == address): #Check if address is a closed loop
                for i in range(PTIMB[address+1]):
                    construct.append(PTIMB[address + i + 2])
                return construct
            else:
                breakpoint("Cannot identify a non-existent array","fatal")
    return(construct)

def addEscInt(item, outpIndex):
    
    result = int(item)
    if(result != ""):
        addItem(outpIndex, result)
                
def splitString(text, delim, outpIndex=None, mode: str = "PTIMB"): # Where the magic happens
    pieces = []
    lastPoint = 0
    i = 0
    n, d = len(text), len(delim)

    while i <= n - d:
        if text[i:i+d] == delim:
            pieces.append(text[lastPoint:i])
            i += d
            lastPoint = i
        else:
            i += 1

    pieces.append(text[lastPoint:])  # remainder (or whole string if no delim)

    if mode == "array":
        return pieces
    elif mode == "PTIMB":
        for p in pieces:
            addEscInt(p, outpIndex)
        
def CitrusReadComponent(byte: int):
    
    if(PTIMB[currentProcReadStateAddress] == 1):
        if(byte == 1): #Debug
            print("Component read successfully")
                    
        if(byte == 2): #Get Interpreter
            print("The current interpreter is Citrus")
            
        if(byte == 3): #PUSH
            PTIMB[currentProcReadStateAddress] = 2

        if(byte == 4): #POP
            PTIMB[currentProcStackAddress + 1 + PTIMB[currentProcStackAddress + 1]] = 0 # Replace top of stack with 0
            PTIMB[currentProcStackAddress + 1] = PTIMB[currentProcStackAddress + 1] - 1 # Tell the stack pointer to move down

    elif(PTIMB[currentProcReadStateAddress] == 2): # Push
        addItem(currentProcStackAddress, byte) # Add the byte to the stack
        PTIMB[currentProcReadStateAddress] = 1 # Return to read state

def alloc(length: int):
    indexof = toInt(PTIMB[PTIMB_AvaiableAddress])   
    newData(toInt(PTIMB[PTIMB_AvaiableAddress]), length)
    return(indexof)

def printRAM(start: int, finish: int, mode = "string"):
    i2 = start
    if(mode == "string"):
        for x in range(finish - start):
            if(type(PTIMB[x]) != int):
                print(f"{PTIMB[x]}    -    [{i2}] <------ WARNING: Not a bit")
            else:
                print(f"{PTIMB[x]}    -    [{i2}]")
            i2 += 1
    elif(mode == "int"):
        for x in range(finish - start):
            if(type(PTIMB[x]) == int):
                print(f"{PTIMB[x]}    -    [{i2}]")
            else:
                print(f"{PTIMB[x]}    -    [{i2}] <------ WARNING: Not a bit")
            i2 += 1
        
def arithmetic(address: int, operation: str, term: int, mode: str = "noWrite"):
    
    value = PTIMB[address]
    if(operation == "*"):
        result = value * term
    elif(operation == "+"):
        result = value + term
    elif(operation == "-"):
        result = value - term
    elif(operation == "/"):
        result = value/term
    elif(operation == "="):
        result = term
    # Decide to write or not
    if(mode == "noWrite"):
        return(result)
    elif(mode == "write"):
        if(result <= 256):
            PTIMB[address] = result
        else:
            breakpoint("Integer is too large to write... Dumping PTIMB")
            printRAM(1, 100)
            breakpoint("Integer is too large to write... PTIMB Dumped")
        
        if(type(PTIMB[address]) != int ):
            print(f"WARNING: Incorrect type assignment put to address {address}")
        return(result)
    
    return(result)

def purgeArray(address: int):
    if(PTIMB[address] != 0): #Check if address is empty
        if(PTIMB[PTIMB[address]] == address): #Check if address is a closed loop
            for i in range(PTIMB[address+1] + 1):
                PTIMB[address + i + 1] = 0
            PTIMB[PTIMB[address]] = 0
            PTIMB[address] = 0
        else:
            breakpoint("Cannot purge a non-existent array","fatal")

def printArray(address: int):
    global Display
    if(PTIMB[address] != 0): #Check if address is empty
        if(PTIMB[PTIMB[address]] == address): #Check if address is a closed loop
            for i in range(PTIMB[address+1]):
                Display.append(PTIMB[address + i + 2])
        else:
            breakpoint("Cannot print a non-existent array","fatal")

def printTCI(input):
    global Display
    Display.append(input)

def endProcess(address):
    assetLocation = getItem(processPTIMBaddress, address)
    for i in getArray(assetLocation):
        purgeArray(i)
    purgeArray(assetLocation)
    PTIMB[address] = 0

def loadProcess(code):
    # Asset Array Key:
    # 0 - Code array address
    # 1 - Stack array address
    # 2 - Instruction Pointer
    # 3 - Read state
    assetAddress = alloc(10) #Create asset array
    codeAddress = alloc(10) # Create container for the code to go in
    stackAddress = alloc(10) # Create stack array
    addItem(assetAddress, codeAddress) # Register code array as asset
    addItem(assetAddress, stackAddress) # Register Stack array as asset
    addItem(assetAddress, codeAddress + 2) # Instruction pointer asset
    addItem(assetAddress, 1) # Read state asset
    splitString(code, "," , codeAddress) # Split code into code array
    addItem(processPTIMBaddress, assetAddress) # Register process after asset array is fully assembled
    
def CitrusTranslate(program: str):
    # Translate the program into a format suitable for execution
    args = splitString(program[1:len(program)-1], "][",0, "array")
    buildProgram = ""
    argIndex = 0
    for arg in args:
        argIndex += 1
        # Process each argument
        match arg:
            case "DEBUG":
                buildProgram += "1"
            case "TEST":
                buildProgram += "2"
            case "PUSH":
                buildProgram += "3"
            case "POP":
                buildProgram += "4"
            case _:
                buildProgram += str(int(arg))
        if(argIndex < len(args)):
            buildProgram += ","

    return buildProgram

def renderTCI():
    global Display

    tacoin.pgHome()
    Display.append(talkbox)
    tacoin.renderList(Display)
    Display.pop()
    pygame.display.flip()

def readKeyboard():
    global talkbox

    if event.type == pygame.TEXTINPUT:
        talkbox += event.text
        renderTCI()

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            talkbox = talkbox[:-1]
            
            renderTCI()
        if event.key == pygame.K_RETURN:
                    Display.append(talkbox)
                    talkbox = ""
                    
                    renderTCI()

# -- START RUNNING --

SystemStart() # Start Tang
tacoin.start() # Start TACOIN Renderer

# Where processes are registered to run
newData(processPTIMBaddress,10)

loadProcess(CitrusTranslate("[PUSH][204][PUSH][255][PUSH][255]"))

# The goal now is to have a process be able to recognize when it has finished and purge all of the arrays and variables it has and all the PTIMB space it has taken up.
# Have a list that records all voids in the PTIMB
# Then have two processes run side by side.

printTCI("Tang v01 | MINFOU") # "What software am I using again?"

while running:
    # Process stuff

    count = PTIMB[processPTIMBaddress + 1]
    #printTCI(count)
    if(count > 0):
        #Find indexes & locations, while updating changed data.
        currentProcAssetsIndex = toInt(getItem(processPTIMBaddress, processPointer))
        currentProcCodeIndex = getIndex(currentProcAssetsIndex, 0)
        currentProcIP = toInt(getItem(currentProcAssetsIndex, 2))
        currentProcIPaddress = getIndex(currentProcAssetsIndex, 2)
        currentProcStackAddress = toInt(getItem(currentProcAssetsIndex, 1))
        currentProcReadState = toInt(getItem(currentProcAssetsIndex, 3))
        currentProcReadStateAddress = getIndex(currentProcAssetsIndex, 3)
        #print(f"DEBUG: Assets Index: {currentProcAssetsIndex}, Code Index: {currentProcCodeIndex}, IP Address: {currentProcIPaddress}, Read State Address: {currentProcReadStateAddress}, Stack Address: {currentProcStackAddress}")

        # Read item
        CitrusReadComponent(PTIMB[currentProcIP])
        arithmetic(currentProcIPaddress, "+", 1, "write")
        #print(f"DEBUG: {currentProcReadState == toInt(PTIMB[currentProcReadStateAddress])}, the value is {toInt(PTIMB[currentProcReadStateAddress])} and {currentProcReadState}")
        #print(f"DEBUG: Instruction pointer: {currentProcIP}")
        if(PTIMB[currentProcCodeIndex + 1] < PTIMB[currentProcIPaddress]):
            endProcess(getIndex(processPTIMBaddress, processPointer))


    # Increase insruction pointer
    processPointer += 1 
    if(processPointer > count):
        processPointer = 0 # They call me chicken parmesan the way I get lost in the sauce.

    # Terminal stuff

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    endTang()
            if event.key == pygame.K_F4:
                if pygame.key.get_mods() & pygame.KMOD_LALT:
                    endTang()

        readKeyboard() # <- Input
    