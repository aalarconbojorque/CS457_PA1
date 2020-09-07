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


def main():

    #StandardInput = False
    CommandsList = []

    #There is NOT standard input file attached
    if sys.stdin.isatty():
        LineInputCommand = input("-->")
        CommandsList.append(LineInputCommand)

    #There is a standard input file attached
    else:
        #Returns a list of commands to execute
        CommandsList = ReadSQLFileInput()
        #StandardInput = True
   
    #With the full CommandsList Process the first command and then delete the first one after it is done
    #CREATE DATABASE db_1;

    while CommandsList :
        ExecuteCommand(CommandsList[0])
        CommandsList.pop(0)
    
    print("All done")

    


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ExecuteCommand(str)
# PURPOSE:           This function reads the command, parses it and executes
#                    the command
# -----------------------------------------------------------------------------
def ExecuteCommand(commandLine):
    print(commandLine)




# ----------------------------------------------------------------------------
# FUNCTION NAME:     ReadSQLFileInput()
# PURPOSE:           This function reads the SQL test file input and parses it
#                    then returns a list of commands to be exected
# -----------------------------------------------------------------------------
def ReadSQLFileInput():
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
