import sys
import json
#Definitions

def breakpoint(msg):
    print(f"BREAKPOINT: {msg}")
    sys.exit()

def SystemStart():
    global PTIMB
    
    global PTIMB_Size
    global maxByteAmount
    maxByteAmount = toInt("1"*byteSize, "string")
    PTIMB_Size = maxByteAmount
    PTIMB = bytearray(PTIMB_Size)
    global running
    running = True
        
        
def toString(number: int) -> str:
    #Converts an integer between 0 and 255 into an 8-bit binary string.  
    if not (0 <= number <= maxByteAmount):
        raise ValueError(f"Number must be between 0 and {maxByteAmount} for an 8-bit byte.")
        
    return f"{number:0{byteSize}b}"
    
def toInt(bit_string, mode = "pass"):
    #Turns an 8-bit binary string into an integer.

    if(mode == "string"):
        if(type(bit_string) == str):
            if(len(bit_string) != byteSize):
                raise ValueError(f"The input string must be exactly {byteSize} bits long.\n     The provided input is {len(bit_string)} bits long. ({bit_string})")
        else:
            raise ValueError("toInt requires a bit string as input.")

        return int(bit_string, 2)
    elif(mode == "pass"):
        return bit_string

def newData(index, length):
    if(PTIMB[index] != 0):
        raise ValueError("PTIMB space is occupied")
    PTIMB[index] = length + index + 2
    PTIMB[index + 1] = 0
    PTIMB[index + length + 2] = index
    PTIMB[PTIMB_AvaiableAddress] = index + length + 3

def insertItem(indexOfData, atPos, inject): #The index of the Array, what you are injecting, and where in the array you want it to go.
    if(PTIMB[PTIMB[indexOfData]] != indexOfData):
        raise ValueError("Selected PTIMB is not closed.")
    if(PTIMB[indexOfData] <= atPos + indexOfData):
        raise ValueError("PTIMB is not long enough to contain data at specified index.")
    PTIMB[indexOfData + 2 + atPos] = inject
    if(PTIMB[indexOfData + 2 + atPos] != inject):
        raise ValueError("Failed to insert item.")

def addItem(index: int, add: str): #Streamlined method for adding to a PTIMB array.
    insertItem(index, toInt(PTIMB[index + 1]), add)
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
      [1] cursor/next-write index
      [2:] data bytes
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

def addEscInt(item, outpIndex):
    result = item[2:len(item)+1]
    if(result != ""):
        addItem(outpIndex, int(item))
                
def splitString(input, delim, outpIndex):
    i = 0
    construct = ""
    lastPoint = 0
    splitCount = 0
    while(i <= len(input) - 1):
        if(len(delim) + i <= len(input)):
            construct = input[i:i+len(delim)]
        else:
            i = len(input) - 2
                
        if(construct == delim):
            
            splitCount += 1
            outPut = input[lastPoint:i]
            
            addEscInt(outPut, outpIndex)
            
            lastPoint = i + 1
            construct = ""
            i += len(delim) - 1
        
        i+=1
        
    if(splitCount >= 1):
        addEscInt(input[lastPoint:len(input)], outpIndex)
        
def CitrusReadComponent(byte: int):
    if(currentProcReadState == 1):
        if(byte == 1): #Debug
            print("Component read successfully")
                    
        if(byte == 2): #Get Interpreter
            print("The current interpreter is Citrus")
            
        if(byte == 3): #PUSH
            breakpoint("PUSH reached")
            PTIMB[currentProcReadStateAddress] = 2

        if(byte == 4): #POP
            PTIMB[currentProcStackAddress + 1 + PTIMB[currentProcStackAddress + 1]] = 0
            PTIMB[currentProcStackAddress + 1] = PTIMB[currentProcStackAddress + 1] - 1

    elif(currentProcReadState == 2):
        addItem(currentProcStackAddress, byte)
        print(f"DEBUG: Added {byte} to stack at address {currentProcStackAddress}")
        PTIMB[currentProcReadStateAddress] = 1
    
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
        PTIMB[address] = result
        if(type(PTIMB[address]) != int ):
            print(f"WARNING: Incorrect type assignment put to address {address}")
        return(result)
    
    return(result)
        
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
    
    
# -- START RUNNING --
 
# Initialize important variables for Processes
processPTIMBaddress = 1
PTIMB_AvaiableAddress = 0
byteSize = 16

SystemStart()

# Where processes are registered to run
newData(processPTIMBaddress,10)

loadProcess("1,2,3,100,3,66")

# Print out a section of ram from beginning to 100 for debugging


processPointer = 0
count = toInt(PTIMB[processPTIMBaddress + 1]) - 1
#print("DEBUG " + str(count))

for x in range(5):
    #Find indexes & locations, while updating changed data.
    currentProcAssetsIndex = toInt(getItem(processPTIMBaddress, processPointer))
    currentProcCodeIndex = getIndex(currentProcAssetsIndex, 0)
    currentProcIP = toInt(getItem(currentProcAssetsIndex, 2))
    currentProcIPaddress = getIndex(currentProcAssetsIndex, 2)
    currentProcStackAddress = toInt(getItem(currentProcAssetsIndex, 1))
    currentProcReadState = toInt(getItem(currentProcAssetsIndex, 3))
    currentProcReadStateAddress = getIndex(currentProcAssetsIndex, 3)
    print(f"DEBUG: Assets Index: {currentProcAssetsIndex}, Code Index: {currentProcCodeIndex}, IP Address: {currentProcIPaddress}, Read State Address: {currentProcReadStateAddress}, Stack Address: {currentProcStackAddress}")

    # Read item
    CitrusReadComponent(PTIMB[currentProcIP])
    arithmetic(currentProcIPaddress, "+", 1, "write")
    print(f"DEBUG: {currentProcReadState == toInt(PTIMB[currentProcReadStateAddress])}, the value is {toInt(PTIMB[currentProcReadStateAddress])} and {currentProcReadState}")
    print(f"DEBUG: Instruction pointer: {currentProcIP}")

    #Increase insruction pointer
    processPointer += 1 
    if(processPointer > count):
        processPointer = 0

printRAM(0,100)