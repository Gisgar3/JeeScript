from sys import *

tokens = []
num_stack = []

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data

def lex(filecontents):
    token = ""
    stringstate = 0
    isexpr = 0
    string = ""
    expr = ""
    n = ""
    filecontents = list(filecontents)
    for char in filecontents:
        token += char
        if token == " ":
            if stringstate == 0:
                token = ""
            else:
                token = " "
        elif token == "\n" or token == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr == ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr == ""
            token = ""
        elif token == "write" or token == "WRITE":
            tokens.append("WRITE")
            token = ""
        elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
            if stringstate == 1:
                string += token
                token = ""
            else:
                expr += token
                token = ""
        elif token == "+" or token == "-" or token == "*" or token == "/" or token == "%" or token == "(" or token == ")":
            if stringstate == 0:  
                isexpr = 1
                expr += token
                token = ""
        elif token == "\"":
            if stringstate == 0:
                stringstate = 1
            elif stringstate == 1:
                tokens.append("STRING: " + string + "\"")
                string = ""
                stringstate = 0
                token = ""
        elif stringstate == 1:
            string += token
            token = ""
        #if token == "DEBUG":
            #if not tokens:
                #print("**INTERNAL ERROR** " + "Debug list is empty; no debug information to display")
            #else:
                #print(tokens)
    #Debugging purposes --> print(tokens)
    return tokens

def evalExpression(expr):
    
    return eval(expr)
    

def correctPrint(resultprint):
    if resultprint[0:6] == "STRING":
        resultprint = resultprint[9:]
        resultprint = resultprint[:-1]
    elif resultprint[0:3] == "NUM":
        resultprint = resultprint[5:]
    elif resultprint[0:4] == "EXPR":
        resultprint = evalExpression(resultprint[6:])
    print(resultprint)

def parse(tokens):
    i = 0
    while(i<len(tokens)):
        if tokens[i] + " " + tokens[i+1][0:6] == "WRITE STRING" or tokens[i] + " " + tokens[i+1][0:3] == "WRITE NUM" or tokens[i] + " " + tokens[i+1][0:4] == "WRITE EXPR":
            if tokens[i+1][0:6] == "STRING":
                correctPrint(tokens[i+1])
            elif tokens[i+1][0:3] == "NUM":
                correctPrint(tokens[i+1])
            elif tokens[i+1][0:4] == "EXPR":
                correctPrint(tokens[i+1])

            i+=2

def run():
    data = open_file(argv[1])
    tokens = lex(data)
    parse(tokens)

run()