import pyglet
from pyglet.window import key


#Definitions
def SystemStart():
    global LIMB
    LIMB = []
    global LIMB_Size
    LIMB_Size = toInt("1"*byteSize)
    for x in range(LIMB_Size):
        LIMB.append("0"*byteSize)
        
    global running
    running = True
        
def toString(number: int) -> str:
    #Converts an integer between 0 and 255 into an 8-bit binary string.  
    if not (0 <= number <= 255):
        raise ValueError("Number must be between 0 and 255 for an 8-bit byte.")
        
    return f"{number:0{byteSize}b}"
    
def toInt(bit_string: str) -> int:
    #Turns an 8-bit binary string into an integer.
    if len(bit_string) != byteSize:
        raise ValueError(f"The input string must be exactly {byteSize} bits long.")
        
    return int(bit_string, 2)

def newData(index, length):
    if(LIMB[index] != "0"*byteSize):
        raise ValueError("LIMB space is occupied")
    LIMB[index] = toString(length + index + 2)
    LIMB[index + 1] = "0"*byteSize
    LIMB[index + length + 2] = toString(index)

def insertItem(indexOfData, atPos, inject): #The index of the Array, what you are injecting, and where in the array you want it to go.
    if len(inject) != byteSize:
        raise ValueError(f"The input string must be exactly {byteSize} bits long.")
    if(toInt(LIMB[toInt(LIMB[indexOfData])]) != indexOfData):
        raise ValueError("Selected LIMB is not closed.")
    if(toInt(LIMB[indexOfData])<=atPos + indexOfData):
        raise ValueError("LIMB is not long enough to contain data at specified index.")

    LIMB[indexOfData + 2 + atPos] = inject
   
def addItem(index, add): #Streamlined method for adding to a LIMB array.
    insertItem(index, toInt(LIMB[index+1]), add)
    indexPointer = toInt(LIMB[index+1]) + 1
    LIMB[index+1] = toString(indexPointer)
    
def getItem(source: int, index: int) -> int:
    return LIMB[source + 2 + index]
    
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
        
def newLIMB(name, length):
    LIMB_Avaiable += length + 3
    addItem(14)
    
        
def loadProcess(code):
    
    splitString(code, "," , processLIMBaddress)

# Initialize important variables for Processes
processLIMBaddress = 1
LIMB_Avaiable = 0
byteSize = 16
#Start of program
SystemStart()

#There are many good reasons not to start data at 0.
newData(processLIMBaddress,10)
newData(14,10)
newData(27,10)

loadProcess(f"{toString(1)},{toString(2)}")

i2 = 0
for x in range(50):
    print(f"{LIMB[x]} ({toInt(LIMB[x])})    -    [{i2}]")
    i2 += 1

instructionPointer = 0
count = toInt(LIMB[2])

"""
while(instructionPointer <= count):
    CitrusReadComponent(getItem(1,instructionPointer))
    instructionPointer += 1 """
    