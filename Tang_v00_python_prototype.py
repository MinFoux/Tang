import pyglet
from pyglet.window import key


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
        
def toString(number: int) -> str:
    #Converts an integer between 0 and 255 into an 8-bit binary string.  
    if not (0 <= number <= maxByteAmount):
        raise ValueError(f"Number must be between 0 and {maxByteAmount} for an 8-bit byte.")
        
    return f"{number:0{byteSize}b}"
    
def toInt(bit_string: str) -> int:
    #Turns an 8-bit binary string into an integer.
    if len(bit_string) != byteSize:
        raise ValueError(f"The input string must be exactly {byteSize} bits long.")
        
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
    
def getItem(source: int, index: int) -> int:
    return PTIMB[source + 2 + index]
    
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
            addItem(outpIndex, input[lastPoint:i])
            
            lastPoint = i + 1
            construct = ""
            i += len(delim) - 1
        
        i+=1
        
    if(splitCount >= 1):
        addItem(outpIndex, input[lastPoint:len(input)])
        
def CitrusReadComponent(byte):
    if len(byte) != byteSize:
        raise ValueError(f"The input string must be exactly {byteSize} bits long.")
    if(byte == toString(1)):
        print("Component read successfully")
        
    if(byte == toString(2)):
        print("The current interpreter is Citrus")
        
def alloc(length):
    indexof = toInt(PTIMB[PTIMB_AvaiableAddress])   
    newData(toInt(PTIMB[PTIMB_AvaiableAddress]), length)
    return(indexof)

def printRAM(start: int, finish: int):
    i2 = start
    for x in range(finish - start):
        print(f"{PTIMB[x]} ({toInt(PTIMB[x])})    -    [{i2}]")
        i2 += 1
    
        
def loadProcess(code):
    # Asset Array Key:
    # 1 - Code array address
    # 2 - Stack array address
    # 3 - Instruction Pointer
    # 4 - Read state
    assetAddress = alloc(10) #Create asset array
    codeAddress = alloc(10) # Create container for the code to go in
    stackAddress = alloc(10) # Create stack array
    addItem(assetAddress, toString(codeAddress)) # Register code array as asset
    addItem(assetAddress, toString(stackAddress)) # Register Stack array as asset
    addItem(assetAddress, toString(0)) # Instruction pointer asset
    addItem(assetAddress, toString(1)) # Read state asset
    splitString(code, "," , codeAddress) # Split code into code array
    addItem(processPTIMBaddress, toString(assetAddress)) # Register process after asset array is fully assembled

# Initialize important variables for Processes
processPTIMBaddress = 1
PTIMB_AvaiableAddress = 0
byteSize = 16
#Start of program
SystemStart()

# Where processes are registered to run
newData(processPTIMBaddress,10)

loadProcess(f"{toString(1)},{toString(2)}")

# printRAM(0,100)

instructionPointer = 0
count = toInt(PTIMB[2])

"""
while(instructionPointer <= count):
    CitrusReadComponent(getItem(1,instructionPointer))
    instructionPointer += 1 """
    