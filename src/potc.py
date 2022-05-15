import sys

# Make sure command is valid
if len(sys.argv) < 2: print("Usage: potc <file>"); exit()
fileExtensions = [".p22", ".p", ".ptrn", ".pt"]
validFileExtension = False
for i in fileExtensions: 
    if sys.argv[1].endswith(i): validFileExtension = True 
if not validFileExtension: print("Valid file extensions: .p22 | .p | .ptrn | .pt"); exit()

# Get file's contents
programContents = str()
with open(sys.argv[1]) as file:
    fileReadlines = file.readlines()
    for i in fileReadlines: programContents += i.strip()

# Scanner Stage 1: Words
scannerStageOne = list()
word = str()
for i in programContents:
    if i.isalpha() or i.isdigit(): word += i; 
    else: 
        if word != "": scannerStageOne.append(word); word = str(); 
        scannerStageOne.append(i)

# Scanner Stage 2: Strings
scannerStageTwo = list()
string = str()
for i in scannerStageOne:
    if not string:
        if i == "\"": string += i 
        else: scannerStageTwo.append(i)
    elif string:
        string += i
        if i == "\"": scannerStageTwo.append(string); string = str()

# Scanner Stage 3: White Space Removal
scannerStageThree = list()
for i in scannerStageTwo:
    if i != " ": scannerStageThree.append(i)

# Scanner Stage 4: Double Char Tokens
scannerStageFour = list()
position = -1
while position < len(scannerStageThree) - 1:
    position += 1
    token = scannerStageThree[position]
    if position > 0: previousToken = scannerStageThree[position-1]
    else: previousToken = ""
    if position < len(scannerStageThree) - 2: nextToken = scannerStageThree[position+1]
    else: nextToken = ""
    if token == ":":
        if nextToken == ":":
            token = token + nextToken
            scannerStageThree.remove(nextToken)
    if token == "}":
        if nextToken == ";":
            token = token + nextToken
            scannerStageThree.remove(nextToken)
    if token == ";":
        if previousToken == "}":
            token = previousToken + token
            scannerStageFour.remove(previousToken)
    scannerStageFour.append(token)

# Scanner Stage 5: Remove empty items
scannerStageFive = list()
for i in scannerStageFour:
    if i != "": scannerStageFive.append(i)

# Set scanner variable : 
# Allows us to add additional stages without
# hurting the tokenizer
scanner = scannerStageFive

# Tokenizer
tokenizer = list()
position = -1
while position < len(scanner) -1:
    position += 1
    token = scanner[position]
    if position > 0: previousToken = scanner[position-1]
    else: previousToken = ""
    if position < len(scanner) - 2: nextToken = scanner[position+1]
    else: nextToken = ""
    if token[0].isalpha(): tokenizer.append([token, "idn", position])
    elif token.isdigit(): tokenizer.append([token, "int", position])
    elif token.startswith("\""): tokenizer.append([token, "str", position])
    else: tokenizer.append([token, "tok", position])

# Parser
ast = list()
def walk(position):
    node = {}
    token = tokenizer[position]
    
    if token[1] == "idn":
        if token[0] == "Return":
            node = {
                "type": "ReturnValue",
                "value": str()
            }
            if position < len(tokenizer)-1: position += 1
            token = tokenizer[position]
            node["value"] = token[0]
            if node != {}: return node
        elif token[0] == "OutputLine":
            node = {
                "type": "OutputLine",
                "value": str()
            }
            if position < len(tokenizer)-1: position += 1
            token = tokenizer[position]
            node["value"] = token[0]
            if node != {}: return node
    elif token[1] == "tok":
        if token[0] == "{":
            node = {
                "type": list(),
                "value":  str(),
                "params": list(),
                "body": list()
            }
            cursorPosition = position
            bracketTypes = ["Function", "Program"]
            while tokenizer[cursorPosition][0] not in bracketTypes:
                cursorPosition -= 1
                if tokenizer[cursorPosition][0] == "Program":
                    node["type"].append(tokenizer[cursorPosition][0])
                    programPosition = cursorPosition
                    node["value"] = tokenizer[programPosition+1][0]
                    while token[0] != "};":
                        if position < len(tokenizer)-1:
                            position += 1
                        if walk(position) != None:
                            node["body"].append(walk(position))
                            token = tokenizer[position]
                            if node != {}: return node
                if tokenizer[cursorPosition][0] == "Function":
                    node["type"].append(tokenizer[cursorPosition][0])
                    functionPosition = cursorPosition
                    if tokenizer[functionPosition-1][0] == "::": node["type"].append(tokenizer[functionPosition-2][0])
                    if tokenizer[functionPosition-3][0] == "Export": node["type"].append("Exported")
                    node["value"] = tokenizer[functionPosition+1][0]
                    while token[0] != "};":
                        if position < len(tokenizer)-1:
                            position += 1
                            token = tokenizer[position]
                        if walk(position) != None:
                            node["body"].append(walk(position))
                    if node != {}: return node
position = -1
while position < len(tokenizer) -1:
    position += 1
    if walk(position) != None:
        ast.append(walk(position))
        break
print(ast)