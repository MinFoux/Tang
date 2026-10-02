import sys
#Definitions
def SystemStart():
    global PTIMB
    PTIMB = []
    global PTIMB_Size
    global maxByteAmount
    maxByteAmount = toInt("1"*byteSize)
    PTIMB_Size = maxByteAmount
    for x in range(PTIMB_Size):
        PTIMB.append("0"*byteSize)
        
    global running
    running = True
    
def breakpoint(msg):
    print(f"BREAKPOINT: {msg}")
    sys.exit()
        
def toString(number: int) -> str:
    #Converts an integer between 0 and 255 into an 8-bit binary string.  
    if not (0 <= number <= maxByteAmount):
        raise ValueError(f"Number must be between 0 and {maxByteAmount} for an 8-bit byte.")
        
    return f"{number:0{byteSize}b}"
    
def toInt(bit_string: str) -> int:
    #Turns an 8-bit binary string into an integer.
    if(type(bit_string) == str):
        if(len(bit_string) != byteSize):
            raise ValueError(f"The input string must be exactly {byteSize} bits long.\n     The provided input is {len(bit_string)} bits long. ({bit_string})")
    else:
        raise ValueError("toInt requires a bit string as input.")

        
    return int(bit_string, 2)

def newData(index, length):
    if(PTIMB[index] != "0"*byteSize):
        raise ValueError("PTIMB space is occupied")
    PTIMB[index] = toString(length + index + 2)
    PTIMB[index + 1] = "0"*byteSize
    PTIMB[index + length + 2] = toString(index)
    PTIMB[PTIMB_AvaiableAddress] = toString(index + length + 3)

def insertItem(indexOfData, atPos, inject): #The index of the Array, what you are injecting, and where in the array you want it to go.
    if len(inject) != byteSize:
        raise ValueError(f"The input string must be exactly {byteSize} bits long.")
    if(toInt(PTIMB[toInt(PTIMB[indexOfData])]) != indexOfData):
        raise ValueError("Selected PTIMB is not closed.")
    if(toInt(PTIMB[indexOfData])<=atPos + indexOfData):
        raise ValueError("PTIMB is not long enough to contain data at specified index.")

    PTIMB[indexOfData + 2 + atPos] = inject
   
def addItem(index: int, add: str): #Streamlined method for adding to a PTIMB array.
    insertItem(index, toInt(PTIMB[index + 1]), add)
    indexPointer = toInt(PTIMB[index + 1]) + 1
    PTIMB[index+1] = toString(indexPointer)
    
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

    result = PTIMB[targetIndex]
    if not isinstance(result, str):
        raise ValueError(f"PTIMB entry at index {targetIndex} is not a bit string: {result!r}")
    if len(result) != byteSize:
        raise ValueError(
            f"PTIMB entry at index {targetIndex} must be exactly {byteSize} bits long; "
            f"got {len(result)} bits ({result})"
        )

    return result

def addEscInt(item, outpIndex):
    if(item[0:2] != "c:"):
        addItem(outpIndex, item)
    else:
        addItem(outpIndex, toString(int(item[2:len(item)+1])))
                
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
        
def CitrusReadComponent(byte):
    if(currentProcReadState == 1):
        if len(byte) != byteSize:
            raise ValueError(f"The input string must be exactly {byteSize} bits long.")
        if(byte == toString(1)):
            print("Component read successfully")
                    
        if(byte == toString(2)):
            print("The current interpreter is Citrus")
            
        if(byte == toString(3)):
            PTIMB[currentProcReadStateAddress] = 2

    elif(currentProcReadState == 2):
        addItem(currentProcStackAddress, byte)
        print(f"DEBUG: Added {byte} to stack at address {currentProcStackAddress}")
    
        
def alloc(length):
    indexof = toInt(PTIMB[PTIMB_AvaiableAddress])   
    newData(toInt(PTIMB[PTIMB_AvaiableAddress]), length)
    return(indexof)

def printRAM(start: int, finish: int):
    i2 = start
    for x in range(finish - start):
        print(f"{PTIMB[x]} ({toInt(PTIMB[x])})    -    [{i2}]")
        i2 += 1
        
def arithmetic(address, operation, term, mode = "noWrite"):
    value = toInt(PTIMB[address])
    if(operation == "*"):
        result = value * term
    elif(operation == "+"):
        result = value + term
    elif(operation == "-"):
        result = value - term
    elif(operation == "/"):
        result = value/term
    if(mode == "noWrite"):
        return(result)
    elif(mode == "write"):
        PTIMB[address] = toString(result)
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
    addItem(assetAddress, toString(codeAddress)) # Register code array as asset
    addItem(assetAddress, toString(stackAddress)) # Register Stack array as asset
    addItem(assetAddress, toString(codeAddress + 2)) # Instruction pointer asset
    addItem(assetAddress, toString(1)) # Read state asset
    splitString(code, "," , codeAddress) # Split code into code array
    addItem(processPTIMBaddress, toString(assetAddress)) # Register process after asset array is fully assembled
    
    
# -- START RUNNING --
 
# Initialize important variables for Processes
processPTIMBaddress = 1
PTIMB_AvaiableAddress = 0
byteSize = 16

SystemStart()

# Where processes are registered to run
newData(processPTIMBaddress,10)

loadProcess("c:1,c:2,c:3,c:133")

# Print out a section of ram from beginning to 100 for debugging
printRAM(0,100)

processPointer = 0
count = toInt(PTIMB[processPTIMBaddress + 1])
print("DEBUG " + str(count))

for x in range(3):
    #Find indexes & locations
    currentProcAssetsIndex = toInt(getItem(processPTIMBaddress, processPointer))
    currentProcCodeIndex = toInt(PTIMB[currentProcAssetsIndex + 2])
    currentProcIP = toInt(getItem(currentProcAssetsIndex, 2))
    currentProcIPaddress = currentProcAssetsIndex + 4
    currentProcStackAddress = toInt(getItem(currentProcAssetsIndex, 1))
    currentProcReadState = toInt(getItem(currentProcAssetsIndex, 3))
    currentProcReadStateAddress = currentProcAssetsIndex + 5

    # Read item

    CitrusReadComponent(PTIMB[currentProcIP])

    arithmetic(currentProcIPaddress, "+", 1, "write")
    print(f"DEBUG: {currentProcReadState == toInt(PTIMB[currentProcReadStateAddress])}, the value is {toInt(PTIMB[currentProcReadStateAddress])} and {currentProcReadState}")
    #Increase insruction pointer
    processPointer += 1 
    if(processPointer > count):
        processPointer = 0
    
    
    