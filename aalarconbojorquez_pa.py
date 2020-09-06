# -----------------------------------------------------------------------------
# FILE NAME:         aalarconbojorquez_pa.py
# USAGE:             python3 aalarconbojorquez_pa.py < PA1_test.sql
# NOTES:             Runs using the standards file input {filename} < PA1_test.sql
#
# MODIFICATION HISTORY:
# Author             Date           Modification(s)
# ----------------   -----------    ---------------
# Andy Alarcon       2020-09-06     1.0 .. Created
# -----------------------------------------------------------------------------

import sys


def main():
    CommandsList = ReadSQLFileInput()

    for line in CommandsList:
        print(line)


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ReadSQLFileInput() d a
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
