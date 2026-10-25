import sys
import os
import json
formatVersion = 1
construct = {}
construct["Default"] = "NONE"
construct["Image"] = "NONE"
print(" - Disk Manager started - ")

def splitString(input, delim):
    i = 0
    construct = ""
    lastPoint = 0
    splitCount = 0
    split = []
    while(i <= len(input) - 1):
        if(len(delim) + i <= len(input)):
            construct = input[i:i+len(delim)]
        else:
            i = len(input) - 2
                
        if(construct == delim):
            
            splitCount += 1
            outPut = input[lastPoint:i]
            
            split.append(outPut)

            lastPoint = i + 1
            construct = ""
            i += len(delim) - 1
        
        i+=1
        
    if(splitCount >= 1):
        split.append(input[lastPoint:len(input)])

    return split

def getKeyword(input):
    keyword = ""
    for i in range(len(input)):
        if(input[i] == ':'):
            break
        keyword += input[i]
    return keyword

def consume(statement, values):
    args = []
    secondVal = values[1]
    key = getKeyword(values[0])
    tempVal = values[0]
    tempVal = tempVal[len(key)+1:len(tempVal)]
    if(tempVal != ""):
        values[0] = tempVal

    args.append(secondVal[len(key)+1:secondVal.find('=')])
    args.append(secondVal[secondVal.find('=') + 1:len(secondVal)])

    if(statement == "init"):
        #The user wants to initialize something
        if(key == "Disk"):
            # The user wants to initialize a disk

            print(f"Disk \"{values[0]}\" initialized to path: {values[1]}")
            if("." in values[0]):
                print("ERROR: Invalid disk name")
                pass
            
            construct[values[0]] = values[1] #Create disk in construct
           
            construct[values[0]+".size"] = 1 #Create necessary variables for the disk
            
            disk_file = open(values[1], "wb") #Create the disk file
            data = b'\x00'*1024
            disk_file.write(data)
            val1 = values[0]

        else:
            # The user wants to initialize something else
            print(f"Initialized {values[0]} as {values[1]}")
            
            
            if(values[0] in construct.keys()):  
                raise ValueError("Initialize (init) can only change existing values.") # Throw error because init should only create, not change values. 
            else:
                construct[val1] = values[1] # Create new value in construct
            
    elif(statement == "fort"): #"fort" is short for "Format", I know it doesn't make any sense but bear with me here
        val1 = values[0] # Store the value for later use
        print(f"Formatted {values[0]} to {values[1]}")
        if(values[0] in construct.keys()):  
            construct[values[0]] = values[1]
            lengVal1 = len(val1)

            # Determine consequence for the construct change
            breakpoint(val1[lengVal1-len(".size"):lengVal1]) 
            # Debugging line, remove later [TOP PRIORITY RN!!!] Change this to get everything after the last "." in the string, this is to determine what consequence the change will have on the disk image.
            if(val1[lengVal1-len(".size"):lengVal1] == ".size"):

                #Opens up the file to rewrite (Increase or decrease size)
                filekey = values[0]
                filekey = filekey[0:len(filekey)-len(".size")]
                breakpoint(f"Filekey: {filekey}")
                disk_file = open(construct[filekey], "wb")
                size = int(values[1]) * 1024
                data = b'\x00'*size
                disk_file.write(data)
                
                
        else:
            
            raise ValueError("Format (fort) can only change existing values.")
            # Throw error because fort should only change, not create values. 
                
    return args

def findParts(input):
    parts = []
    for i in range(len(input)):
        if input[i] == '{':
            parts.append(input[:i])
            parts.append(input[i+1:len(input)-1])
            return parts

    return [input]

def writeDisk(data, address):
    with open(construct[construct["Default"]], "r+b") as f:
        f.seek(address)     
        f.write(bytes([data]))

def readDisk(address):
    with open(construct[construct["Default"]], "rb") as f:
        f.seek(address)
        return f.read(1)[0]

# Start

with open("TangDisk\\TangDiskSettings.cfg","r") as get_file:
    file_content = get_file.read()

#Clean for splitting
file_content = file_content.replace("\n", "")
#Split
args = splitString(file_content, ";")

for arg in args:
    if(arg != ""):
        # Get rid of spaces
        arg = arg.replace(" ", "")
        # Get the main of argument
        parts = findParts(arg)
        # Get the secondary of argument
        values = splitString(parts[1], "=")
        consume(parts[0], values)

writeDisk(formatVersion, 0) #Identify format version and write to disk

# Follow instructions from disk Image

if(construct["Image"] != "NONE"):
    # Process the disk image
    pass
else:
    writeDisk(255, 1)
    writeDisk(255, 2)

# Communicate results to Tang as JSON
y1 = json.dumps(construct)
try:
    with open("TangDisk\\TangDiskCompiledSettings.json","w") as get_file:
        get_file.write(y1)
except Exception as e:
    print(f"Error occurred while writing to file: {e}")

print(" - Disk Manager ended - ")