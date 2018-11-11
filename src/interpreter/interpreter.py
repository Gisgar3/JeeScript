# COPYRIGHT (C) GAVIN ISGAR 2018
# JEESCRIPT V1.1.0 INTERPRETER

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
    ismode = 0
    isfunc = 0
    string = ""
    expr = ""
    funcdata = ""

    filecontents = list(filecontents)
    for char in filecontents:
        token += char
        if token == " ":
            if stringstate == 0:
                token = ""
            else:
                token = " "
        # NEWLINE/EOF ---
        elif token == "\n" or token == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr == ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr == ""
            token = ""
        # ---------------
        # ACTIONS ---
        elif token == "write" or token == "WRITE":
            tokens.append("WRITE")
            token = ""
        elif token == "mode" or token == "MODE":
            tokens.append("MODE")
            ismode = 1
            token = ""
        # -----------
        # NUMBERS/EXPR/LETTERS ---
        elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
            if stringstate == 1:
                string += token
                token = ""
            else:
                expr += token
                token = ""
        elif token == "+" or token == "-" or token == "*" or token == "/" or token == "%" or token == "(" or token == ")":
            if token == ")" and isfunc == 1:
                tokens.append("FUNCDATA: " + funcdata[0:-1])
                funcdata = ""
                isfunc = 0
                token = ""
            elif stringstate == 0:  
                isexpr = 1
                expr += token
                token = ""
        # ------------------------
        # STRINGS ---
        elif token == "\"":
            if stringstate == 0:
                stringstate = 1
            elif stringstate == 1:
                if isfunc == 1:
                    funcdata += token
                    token = ""
                elif isfunc == 0:
                    tokens.append("STRING: " + string + "\"")
                    string = ""
                    stringstate = 0
                    token = ""
        elif stringstate == 1:
            if isfunc == 1:
                funcdata += token
                token = ""
            elif isfunc == 0:
                string += token
                token = ""
        # -----------
        # FUNCTIONS ---
        elif token == "LOAD" or token == "load":
            isfunc = 1
            tokens.append("FUNCTION [LOAD]")
            token = ""
        # -------------
        # MODES TYPES ---
        elif token == "DEBUG":
            if ismode == 1:
                tokens.append("DEBUG")
                ismode = 0
                token = ""
        # ---------------
        
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
        elif tokens[i] + " " + tokens[i+1][0:5] == "MODE DEBUG":
            if tokens[i+1][0:5] == "DEBUG":
                print(tokens)
                i+=2
        elif tokens[i][0:8] + " " + tokens[i+1][0:8] == "FUNCTION FUNCDATA":
            if tokens[i] == "FUNCTION [LOAD]":
                lex(open_file(tokens[i+1][11:]))
            i+=2


def run():
    if argv[1].endswith(".jee"):
        data = open_file(argv[1])
        tokens = lex(data)
        # "DEBUG" method is currently a placeholder; will change if new argv arguments are added
        # This method is not dependent on when the tokens are appended; the tokens are appended before this is ran
        if argv.__contains__("DEBUG") or argv.__contains__("debug"):
            print(tokens)
        else:
            print("**ARGS** No arguments are being used; placeholder for background-logging")
        parse(tokens)
    else:
        print("**ERROR** Only JeeScript files can be executed.")

run()