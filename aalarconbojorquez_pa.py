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
# -----------------------------------------------------------------------------

import sys
import re
import os


def main():

    # List that holds all commands that will executed
    CommandsList = []

    # There is NOT standard input file attached
    if sys.stdin.isatty():
        LineInputCommand = str(input("--> "))
        CommandsList.append(LineInputCommand)

    # There is a standard input file attached
    else:
        # Returns a list of commands to execute
        CommandsList = ReadCommandsFileInput()

    # With the full CommandsList Process the first command and then delete the first one after it is done

    # LEAVE WHEN .EXIT
    while CommandsList:
        ExecuteCommand(CommandsList[0])
        CommandsList.pop(0)

    print("All done")


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ExecuteCommand(str)
# PURPOSE:           This function reads the command, parses it and executes
#                    the command
# -----------------------------------------------------------------------------
def ExecuteCommand(commandLine):

    unalteredCommandLine = commandLine
    # CREATE DATABASE db_1;

    commandLine = ParseCommandByWord(commandLine)

    # Use each parsed keyword and execute the corresponding command
    
    if commandLine[0].lower() == "create":

        if commandLine[1].lower() == "database":
            print("CREATE Database -> " + commandLine[2])
      
        elif commandLine[1].lower() == "table":
            print("CREATE Table -> " + commandLine[2])
        else:
            print("!Failed CREATE command argumments not recognized")
    
    elif commandLine[0].lower() == "drop":
       
        if commandLine[1].lower() == "database":
            print("DROP Database -> " + commandLine[2])
           
        elif commandLine[1].lower() == "table":
            print("DROP Table -> " + commandLine[2])
        else:
            print("!Failed DROP command argumments not recognized")

    elif commandLine[0].lower() == "alter":
           
        if commandLine[1].lower() == "table":
            print("ALTER Table -> " + commandLine[2])
        else:
            print("!Failed ALTER command argumments not recognized")

    elif commandLine[0].lower() == "use":
           
        print("USE Database -> " + commandLine[1])
        

    elif commandLine[0].lower() == "select":
           
        if commandLine[1].lower() == "*":
            print("SELECT ALL")
        else:
            print("!Failed SELECT command argumments not recognized")


    else:
        print("!Failed Commands not recognized")


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
