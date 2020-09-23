# -----------------------------------------------------------------------------
# FILE NAME:         aalarconbojorquez_pa.py
# USAGE:             python3 aalarconbojorquez_pa.py < PA1_test.sql
# NOTES:             Runs using the standards file input {filename} < PA1_test.sql
#                    or line by line input python3 aalarconbojorquez_pa.py
#
# MODIFICATION HISTORY:
# Author             Date           Modification(s)
# ----------------   -----------    ---------------
# Andy Alarcon       2020-09-09     1.0 .. Created, implemented standard input
# Andy Alarcon       2020-09-11     1.1 .. implemented line by line input check
#                                          and first iteration of parsing check
# Andy Alarcon       2020-09-13     1.2 .. Added DB and table creation, added drop
#                                          for DB and table
# Andy Alarcon       2020-09-15     1.3 .. Added table query feature
# Andy Alarcon       2020-09-18     1.4 .. Added table update feature
# Andy Alarcon       2020-09-21     1.5 .. Fixed a parsing bug
# Andy Alarcon       2020-09-23     1.6 .. Added a drop database condition
# -----------------------------------------------------------------------------

import sys
import re
import os
import shutil

# Global variable to keep track of the current DB in use
GlobalCurrentDirectory = ""


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
    # Standard input
    if StandardInputisActive:
        while CommandsList[0].lower() != ".exit":
            ExecuteCommand(CommandsList[0])
            CommandsList.pop(0)

    #Line by Line input
    else:
        while LineInputCommand.lower() != ".exit":
            ExecuteCommand(LineInputCommand)
            LineInputCommand = str(input("--> "))

    print("All done.")


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ExecuteCommand(str)
# PURPOSE:           This function reads a single command, parses it and executes
#                    the command
# -----------------------------------------------------------------------------


def ExecuteCommand(commandLine):

    unalteredCommandLine = commandLine

    # Error message that is displayed when a command line has an
    # invalid number of arguments
    argumentErrorMessage = "!Failed a syntax error occured"

    # Parse the single command and returns a list
    commandLine = ParseCommandByWord(commandLine)

    # Use each parsed keyword and execute the corresponding command
    if not commandLine:
        print('', end='')
    else:

        # If the first keyword is create
        if commandLine[0].lower() == "create":

            # Check the remaining ones and execute or display an error if invalid
            try:
                if commandLine[1].lower() == "database":
                    CreateDatabase(commandLine[2])
                elif commandLine[1].lower() == "table":
                    CreateTable(commandLine[2], unalteredCommandLine)
                else:
                    print("!Failed CREATE command argumments not recognized")
            except:
                print(argumentErrorMessage)

        # If the first keyword is drop
        elif commandLine[0].lower() == "drop":

            # Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "database":
                    DropDatabase(commandLine[2])
                elif commandLine[1].lower() == "table":
                    DropTable(commandLine[2])
                else:
                    print("!Failed DROP command argumments not recognized")

            except:
                print(argumentErrorMessage)

        # If the first keyword is alter
        elif commandLine[0].lower() == "alter":
            # Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "table":
                    AlterTable(unalteredCommandLine, commandLine[2:])
                else:
                    print("!Failed ALTER command argumments not recognized")

            except:
                print(argumentErrorMessage)

        # If the first keyword is use
        elif commandLine[0].lower() == "use":
            # Check the remaining ones and execute or display an error
            try:
                UseDatabase(commandLine[1])
            except:
                print(argumentErrorMessage)

        # If the first keyword is select
        elif commandLine[0].lower() == "select":
            # Check the remaining ones and execute or display an error
            try:
                if commandLine[1].lower() == "*" and commandLine[2].lower() == "from":
                    SelectCommand(commandLine[3])
                else:
                    print("!Failed SELECT command argumments not recognized")
            except:
                print(argumentErrorMessage)

        # If the first keyword was not recognized above display an error
        else:
            print("!Failed command : '" + commandLine[0] + "' not recognized")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     AlterTable(tblName)
# PURPOSE:           This function executes the alter table command
# -----------------------------------------------------------------------------


def AlterTable(OGcommandLine, commandsList):

    if len(commandsList) > 4:
        tblName = commandsList[0]
        # Find the text between the command ADD and ; for variable argument
        line = OGcommandLine.lower()
        line = re.search(r'add\s\s*(.*)\s*;', line).group(1)

        global GlobalCurrentDirectory
        if not GlobalCurrentDirectory:
            print("!Failed a database is currently not in use")
        else:
            # Check if the table/file exists
            if os.path.exists(GlobalCurrentDirectory + "/" + tblName):
                # append the add argument
                file = open(GlobalCurrentDirectory + "/" + tblName, "a")
                file.write(" | " + line)
                file.close()
                print("Table " + tblName + " modified.")
            else:
                print("!Failed to modify table " +
                      tblName + " because it does not exist.")

    else:
        print("!Failed invalid number of arguments")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     DropTable(tblName)
# PURPOSE:           This function executes the drop table command
# -----------------------------------------------------------------------------


def DropTable(tblName):
    global GlobalCurrentDirectory
    if not GlobalCurrentDirectory:
        print("!Failed a database is currently not in use")
    else:
        # Check if the table/file exists
        if os.path.exists(GlobalCurrentDirectory + "/" + tblName):
            try:
                os.remove(GlobalCurrentDirectory + "/" + tblName)
                print("Table " + tblName + " deleted.")
            except:
                print("!Failed to delete the table due to an error")
        else:
            print("!Failed to delete " + tblName +
                  " because it does not exist.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     DropDatabase(DBname)
# PURPOSE:           This function executes the drop database command
# -----------------------------------------------------------------------------


def DropDatabase(DBname):
    # Check if the folder exists
    if os.path.exists(DBname):

        try:
            # Remove directory
            shutil.rmtree(DBname)

            # If the global database was dropped, reset global variable
            global GlobalCurrentDirectory
            if GlobalCurrentDirectory == DBname :
                GlobalCurrentDirectory = ""

            print("Database " + DBname + " deleted.")
        except:
            print("!Failed to delete the database due to an error")

    else:
        print("!Failed to delete " + DBname + " because it does not exist.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     SelectCommand(tblName)
# PURPOSE:           This function executes the select command
# -----------------------------------------------------------------------------


def SelectCommand(tblName):
    global GlobalCurrentDirectory
    if not GlobalCurrentDirectory:
        print("!Failed a database is currently not in use")
    else:
        # Check if the table/file exists
        if not os.path.exists(GlobalCurrentDirectory + "/" + tblName):

            print("!Failed to query table " +
                  tblName + " because it does not exist.")

        else:
            file = open(GlobalCurrentDirectory + "/" + tblName, "r")
            LinesRead = file.readline()
            print(LinesRead)
            file.close()
# ----------------------------------------------------------------------------
# FUNCTION NAME:     UseDatabase(DBname)
# PURPOSE:           This function executes the database use command
# -----------------------------------------------------------------------------


def UseDatabase(DBname):
    # Check if the folder exists
    if os.path.exists(DBname):
        global GlobalCurrentDirectory
        GlobalCurrentDirectory = DBname
        print("Using database " + DBname + ".")
    else:
        print("!Failed to use database " + DBname +
              " because it does not exist.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     ParseCommandByPara()
# PURPOSE:           This function parses a string for table creation, returns a list
# -----------------------------------------------------------------------------


def ParseCommandByPara(line):

    # Parse Everything within (.....); Then split by comma
    line = re.search(r'\((.*?)\);', line).group(1)
    line = line.split(',')

    # Remove any leading whitespaces
    for i, _ in enumerate(line):
        line[i] = line[i].strip()

    return line
# ----------------------------------------------------------------------------
# FUNCTION NAME:     CreateTable(tblName, OGCommandLine)
# PURPOSE:           This function executes the database creation command
# -----------------------------------------------------------------------------


def CreateTable(tblName, OGCommandLine):

    global GlobalCurrentDirectory
    if not GlobalCurrentDirectory:
        print("!Failed a database is currently not in use")
    else:

        # Try and Parse the string "(arg arg arg);""
        argumentsParsed = True
        try:
            argumentList = ParseCommandByPara(OGCommandLine)

            # Check the number of args must be >= 2
            argumentsCheckList = []
            for i, _ in enumerate(argumentList):
                argumentsCheckList.append(argumentList[i].split())
                if len(argumentsCheckList[i]) < 2:
                    argumentsParsed = False

        # If it fails trigger flag
        except:
            argumentsParsed = False

        # Check if tblName is invalid or flag has been triggered
        if tblName == "(" or not tblName or argumentsParsed == False:
            print("!Failed a syntax error occured")

        else:
            # Check if the table/file exists
            if not os.path.exists(GlobalCurrentDirectory + "/" + tblName):

                file = open(GlobalCurrentDirectory + "/" + tblName, "w")
                print("Table " + tblName + " created.")

                for i, _ in enumerate(argumentList):

                    if len(argumentList) - 1 == i:
                        file.write(argumentList[i])
                    else:
                        file.write(argumentList[i] + " | ")

                file.close()
            else:
                print("!Failed to create table " +
                      tblName + " because it already exists.")
# ----------------------------------------------------------------------------
# FUNCTION NAME:     CreateDatabase(DBname)
# PURPOSE:           This function executes the database creation command
# -----------------------------------------------------------------------------


def CreateDatabase(DBname):
    # First check if the DB name is invalid
    if DBname == ";" or not DBname:
        print("!Failed database name was invalid")

    else:
        # Check if the foler exists
        if not os.path.exists(DBname):
            os.mkdir(DBname)
            print("Database " + DBname + " created.")
        else:
            print("!Failed to create database " +
                  DBname + " because it already exists.")
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
