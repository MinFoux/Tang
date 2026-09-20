import pyglet
from pyglet.window import key


#Definitions
def SystemStart():
    global LIMB
    LIMB = []
    global LIMB_Size
    LIMB_Size = 256
    for x in range(LIMB_Size):
        LIMB.append("00000000")
        
    global running
    running = True
        
def to8string(number: int) -> str:
    #Converts an integer between 0 and 255 into an 8-bit binary string.
    if not (0 <= number <= 255):
        raise ValueError("Number must be between 0 and 255 for an 8-bit byte.")
        
    return f"{number:08b}"
    
def toInt8(bit_string: str) -> int:
    #Turns an 8-bit binary string into an integer.
    if len(bit_string) != 8:
        raise ValueError("The input string must be exactly 8 bits long.")
        
    return int(bit_string, 2)

def newData(index, length):
    if(LIMB[index] != "00000000"):
        raise ValueError("LIMB space is occupied")
    LIMB[index] = to8string(length + index + 2)
    LIMB[index + 1] = "00000000"
    LIMB[index + length + 2] = to8string(index)

def insertItem(indexOfData, atPos, inject): #The index of the Array, what you are injecting, and where in the array you want it to go.
    if len(inject) != 8:
        raise ValueError("The input string must be exactly 8 bits long.")
    if(toInt8(LIMB[toInt8(LIMB[indexOfData])]) != indexOfData):
        raise ValueError("Selected LIMB is not closed.")
    if(toInt8(LIMB[indexOfData])<=atPos + indexOfData):
        raise ValueError("LIMB is not long enough to contain data at specified index.")

    LIMB[indexOfData + 2 + atPos] = inject
   
def addItem(index, add): #Streamlined method for adding to a LIMB array.
    insertItem(index, toInt8(LIMB[index+1]), add)
    indexPointer = toInt8(LIMB[index+1]) + 1
    LIMB[index+1] = to8string(indexPointer)
    
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
    if len(byte) != 8:
        raise ValueError("The input string must be exactly 8 bits long.")
    if(byte == "00000001"):
        print("Component read successfully")
        
    if(byte == "00000010"):
        print("The current interpreter is Citrus Read")
        
def loadProcess(code):
    splitString(code, "," , processLIMBaddress)
    
processLIMBaddress = 1
#Start of program
SystemStart()

#There are many good reasons not to start data at 0.
newData(processLIMBaddress,10)
newData(14,1)

loadProcess("00000001,00000010")


instructionPointer = 0
count = toInt8(LIMB[2])

while(instructionPointer <= count):
    CitrusReadComponent(getItem(1,instructionPointer))
    instructionPointer += 1 
    