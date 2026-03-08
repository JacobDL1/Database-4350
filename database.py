import os #used for os.path.exists()
import sys #used for sys.stdout.flush()

FILE = "data.db"

def loadDB(dbValues):
    """Uses data.db to rebuild dbValues for memory persistence"""
    dbValues.clear()
    if os.path.exists(FILE): #if data.db exists, each line is read, and the key value pair is appended to dbValues
        try:
            with open(FILE, "r", encoding="utf-8") as f: #opens using utf-8 encoding to parse file properly
                for i in f:
                    dbEntry = i.strip().replace('\r', '').split(maxsplit=2) #strip and split at most 2 times, replace all '\r' with nothing
                    if len(dbEntry) < 3 or dbEntry[0] != "SET": #skip empty or miswritten lines
                        continue
                    key = dbEntry[1]
                    value = dbEntry[2]
                    duplicateCheck(dbValues, key, value)
        except OSError as e: #error handling incase file opening fails
            print(f"Error when reading database: {e}", file=sys.stderr)

def duplicateCheck(dbValues, key, value):
    """Appends new entry or updates existing key, uses last write wins"""
    for i in dbValues: #compares key value from data.db to those already in dbValues, only appends unique keys
        if i[0] == key:
            i[1] = value
            return
    dbValues.append([key, value])

def setKeyValue(dbValues, key, value):
    """Updates dbValues with key-value pair and adds entry to data.db"""
    duplicateCheck(dbValues, key, value)

    try:
        with open(FILE, "a", encoding="utf-8") as f: #opens and writes to data.db, opens using utf-8 encoding to parse file properly
            f.write(f"SET {key} {value}\n")
            f.flush() #used for making sure SET is complete by the time GET is used for gradebot
            os.fsync(f.fileno()) #used for making sure SET is complete by the time GET is used for gradebot
    except OSError as e: #error handling incase file opening fails
        print(f"Error when writing database: {e}", file=sys.stderr)

def getKeyValue(dbValues, key):
    """Update dbValues for accuracy, then print value of key"""
    loadDB(dbValues)
    for i in dbValues: #comapres key to keys in currValues, prints associated value if found
        if i[0] == key:
            print(i[1])
            sys.stdout.flush()
            return
    print("")
    sys.stdout.flush()

def main():
    """Loops to take user input, calls necessary functions to respond"""
    dbValues = [] #stores all set command key value pairs
    loadDB(dbValues)

    while True:
        userInput = sys.stdin.buffer.readline() #reads raw bytes instead of parsing using input() for more accurate input

        if not userInput: #EOF detection
            break
        userInput = userInput.decode("utf-8", errors = "replace").strip().replace("\r", "") #decodes user input then strips user input

        if not userInput: #skip blank lines
            continue
        words = userInput.split(maxsplit=2) #split at most 2 times

        if words[0].upper() == "SET" and len(words) >= 3: #use upper so input is case insensitive, make sure there aren't too many arguements
            setKeyValue(dbValues, words[1], words[2])
        elif words[0].upper() == "GET" and len(words) >= 2:
            getKeyValue(dbValues, words[1])
        elif words[0].upper() == "EXIT":
            break
        sys.stdout.flush()
                    
if __name__ == "__main__":
    main()