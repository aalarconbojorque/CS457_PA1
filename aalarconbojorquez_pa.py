# -----------------------------------------------------------------------------
# FILE NAME:         aalarconbojorquez_pa.py
# USAGE:             python3 aalarconbojorquez_pa.py < PA1_test.sql
# NOTES:             Runs using the standards file input {filename} < PA1_test.sql
#
# MODIFICATION HISTORY:
# Author             Date           Modification(s)
# ----------------   -----------    ---------------
# Andy Alarcon       2020-09-06     1.0 .. Created, implemented standard input
# Andy Alarcon       2020-09-07     1.1 .. implemented line by line input check
#                                          and first iteration of parsing check
# -----------------------------------------------------------------------------

import sys
import re
import os


def main():

    # List that holds all commands that will executed
    CommandsList = []
    StandardInputisActive = False

    # There is NOT standard input file attached
    if sys.stdin.isatty():

        try:
            LineInputCommand = str(input("--> "))
        except:
            print("Invalid Input Please Try again")

        CommandsList.append(LineInputCommand)

    # There is a standard input file attached
    else:
        # Returns a list of commands to execute
        CommandsList = ReadCommandsFileInput()
        StandardInputisActive = True

    # With the full CommandsList Process the first command and then delete the first one after it is done

    if StandardInputisActive:
        while CommandsList[0].lower() != ".exit":
            ExecuteCommand(CommandsList[0])
            CommandsList.pop(0)

    else:
        while LineInputCommand.lower() != ".exit":
            ExecuteCommand(LineInputCommand)
            LineInputCommand = str(input("--> "))

    # # LEAVE WHEN .EXIT
    # while CommandsList:
    #     ExecuteCommand(CommandsList[0])
    #     CommandsList.pop(0)

    print("All done")


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ExecuteCommand(str)
# PURPOSE:           This function reads a single command, parses it and executes
#                    the command
# -----------------------------------------------------------------------------
def ExecuteCommand(commandLine):

    unalteredCommandLine = commandLine

    #Error message that is displayed when a command line has an
    #invalid number of arguments
    argumentErrorMessage = "!Failed a syntax error occured"

    #Parse the single command and returns a list
    commandLine = ParseCommandByWord(commandLine)

    # Use each parsed keyword and execute the corresponding command
    if not commandLine:
        print('', end='')
    else:
        #If the first keyword is create
        if commandLine[0].lower() == "create":
            
            #Check the remaining ones and execute or display an error if invalid
            try:
                if commandLine[1].lower() == "database":
                    CreateDatabase(commandLine[2])
                elif commandLine[1].lower() == "table":
                    CreateTable(commandLine[2], unalteredCommandLine)
                else:
                    print("!Failed CREATE command argumments not recognized")
            except:
                print(argumentErrorMessage)

        #If the first keyword is drop
        elif commandLine[0].lower() == "drop":
            
            #Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "database":
                    print("DROP Database -> " + commandLine[2])
                elif commandLine[1].lower() == "table":
                    print("DROP Table -> " + commandLine[2])
                else:
                    print("!Failed DROP command argumments not recognized")

            except:
                print(argumentErrorMessage)

        #If the first keyword is alter
        elif commandLine[0].lower() == "alter":
            #Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "table":
                    print("ALTER Table -> " + commandLine[2])
                else:
                    print("!Failed ALTER command argumments not recognized")

            except:
                print(argumentErrorMessage)

        #If the first keyword is use
        elif commandLine[0].lower() == "use":
             #Check the remaining ones and execute or display an error
            try:
                print("USE Database -> " + commandLine[1])
            except:
                print(argumentErrorMessage)
        #If the first keyword is select
        elif commandLine[0].lower() == "select":
            #Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "*":
                    print("SELECT ALL")
                else:
                    print("!Failed SELECT command argumments not recognized")
            except:
                print(argumentErrorMessage)

        #If the first keyword was not recognized above display an error
        else:
            print("!Failed command : '" + commandLine[0] + "' not recognized")


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ParseCommandByPara()
# PURPOSE:           This function parses a string for table creation, returns a list
# -----------------------------------------------------------------------------
def ParseCommandByPara(line):

    return line
# ----------------------------------------------------------------------------
# FUNCTION NAME:     CreateTable(tblName, OGCommandLine)
# PURPOSE:           This function executes the database creation command
# -----------------------------------------------------------------------------
def CreateTable(tblName, OGCommandLine):
    #First check if the DB name is invalid
    if tblName == ";" or not tblName :
        print("!Failed table name was invalid")

    else :
        # Check if the table/file exists
        if not os.path.exists(tblName):
            file = open(tblName, "w") 
            argumentList = ParseCommandByPara(OGCommandLine)
            file.close() 
        else:
            print("!Failed to create table " + tblName + " because it already exists.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     CreateDatabase(DBname)
# PURPOSE:           This function executes the database creation command
# -----------------------------------------------------------------------------
def CreateDatabase(DBname):
    #First check if the DB name is invalid
    if DBname == ";" or not DBname :
        print("!Failed database name was invalid")

    else :
        # Check if the foler exists
        if not os.path.exists(DBname):
            os.mkdir(DBname)
            print("Database " + DBname + " created.")
        else:
            print("!Failed to create database " + DBname + " because it already exists.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     ParseCommandByWord()
# PURPOSE:           This function parses a string by word and removes any
#                    blanks or spaces, returns a list
# -----------------------------------------------------------------------------
def ParseCommandByWord(line):
    # Split the input by word
    line = re.split(r'(\W+)', line)
    # Remove any leading whitespaces from the list
    for i, _ in enumerate(line):
        line[i] = line[i].strip()
    # Remove any blanks from the list
    line = list(filter(None, line))

    return line
# ----------------------------------------------------------------------------
# FUNCTION NAME:     ReadCommandsFileInput()
# PURPOSE:           This function reads the SQL test file input and parses it
#                    then returns a list of commands to be exected
# -----------------------------------------------------------------------------
def ReadCommandsFileInput():
    # Read in the file lines via standard input
    FileInputLines = sys.stdin.readlines()
    # New List which will contain the commands that will be executed
    FileInputCommands = []

    for line in FileInputLines:
        # Ignore lines that are blank or are comments
        if line == '\r\n' or "--" in line:
            pass
        # Remove newline from current line and append to the commands list
        else:
            temp_line = line.replace('\r\n', '')
            FileInputCommands.append(temp_line)

    return FileInputCommands


if __name__ == "__main__":
    main()
