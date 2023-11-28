variables = []


def compile(path: str):
    code: str = readCode(path)
    print(code)
    with (open('final.dart','w') as file):
        file.write(code)


def readCode(path: str) -> str:
    code: str = ""
    numSpaces = 0
    with (open(path, "r") as file):
        lines = file.readlines()
        lines.append("\n")
        for line in lines:
            thisSpaces = line.count("    ")
            line = replaceTokens(line)

            # Handles Variables
            line = handleVariables(line)
        
            # replaces indents with {
            if thisSpaces == numSpaces:
                code += line
            elif thisSpaces < numSpaces:
                code += line + "}\n"*(numSpaces-thisSpaces)
            else: code+=line
            numSpaces = thisSpaces
    return code


def replaceTokens(code: str) -> str:
    replaceDict = {
        "while(": "while",
        "for(": "for",
        "for": "for(",
        "while": "while(",
        "):": ":",
        ":": "){",
        "def": parseDataType(code),
    }
    for key in (replaceDict.keys()):
        code = code.replace(key, replaceDict[key])
        code = removeDatatype(code)
    return code


def parseDataType(data: str) -> str:
    if (data.count("->") > 0):
        dataType = data.split("->")[1].replace(":", "").replace("\n", "")
        dataTypeDict = {"str": "String"}
        if dataType in dataTypeDict.keys():
            return dataTypeDict[dataType]
        else:
            return dataType
    return ""


def removeDatatype(data: str):
    if (data.count("->") > 0):
        return data.replace(data.split("->")[1].split(":")[0], "").replace("->", "")
    return data

def handleVariables(line:str):
    if line.count("=") == 1:
        variableName = line.split("=")[0].replace(" ", "")
        if variableName not in variables:
            variables.append(variableName)
            varindex = line.index(variableName)
            line = line[:varindex]+"dynamic " + line[varindex:].replace("\n","")+ ";"+"\n"
    return line

compile("test.py")