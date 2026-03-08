"""
Program that allows user to use SET commands to append data to a file for persistent storage.
Program also allow use of GET to retrieve a value based on user-provided key, and the use of an EXIT command.

Made by: Jacob Lamb, 11723480
"""

import os #used for os.path.exists()
import sys #used for sys.stdout.flush()

FILE = "data.db"
SET = "SET"
GET = "GET"
EXIT = "EXIT"

class KeyValueStore:
    """Key-value store with data.db serving as persistent storage"""

    def __init__(self, filePath: str = FILE) -> None: #constructor for the class
        self.filePath = filePath
        self.dbValues: list[list[str]] = []
        self.loadDB()
    
    def loadDB(self) -> None:
        """Uses data.db to rebuild dbValues for memory persistence"""
        self.dbValues.clear()
        if os.path.exists(self.filePath): #if data.db exists, each line is read, and the key value pair is appended to dbValues
            try:
                with open(self.filePath, "r", encoding="utf-8") as f: #opens using utf-8 encoding to parse file properly
                    for line in f:
                        dbEntry = line.strip().replace('\r', '').split(maxsplit=2) #strip and split at most 2 times, replace all '\r' with nothing
                        if len(dbEntry) < 3 or dbEntry[0] != SET: #skip empty or miswritten lines
                            continue
                        key = dbEntry[1]
                        value = dbEntry[2]
                        self.duplicateCheck(key, value)
            except OSError as e: #error handling incase file opening fails
                raise OSError(f"Error when reading from database: {e}") from e

    def duplicateCheck(self, key: str, value: str) -> None:
        """Appends new entry or updates existing key, uses last write wins"""
        for entry in self.dbValues: #compares key value from data.db to those already in dbValues, only appends unique keys
            if entry[0] == key:
                entry[1] = value
                return
        self.dbValues.append([key, value])

    def setKeyValue(self, key: str, value: str) -> None:
        """Updates dbValues with key-value pair and adds entry to data.db"""
        self.duplicateCheck(key, value)

        try:
            with open(self.filePath, "a", encoding="utf-8") as f: #opens and writes to data.db, opens using utf-8 encoding to parse file properly
                f.write(f"SET {key} {value}\n")
                f.flush() #used for making sure SET is complete by the time GET is used for gradebot
                os.fsync(f.fileno()) #used for making sure SET is complete by the time GET is used for gradebot
        except OSError as e: #error handling incase file opening fails
            raise OSError(f"Error when writing to database: {e}") from e

    def getKeyValue(self, key: str) -> str:
        """Update dbValues for accuracy, then print value of key"""
        self.loadDB()
        for entry in self.dbValues: #comapres key to keys in currValues, prints associated value if found
            if entry[0] == key:
                return entry[1]
        return ""

def main() -> None:
    """Loops to take user input, calls necessary functions to respond"""
    kvDatabase = KeyValueStore()

    while True:
        userInput = sys.stdin.buffer.readline() #reads raw bytes instead of parsing using input() for more accurate input

        if not userInput: #EOF detection
            break
        userInput = userInput.decode("utf-8", errors = "replace").strip().replace("\r", "") #decodes user input then strips user input

        if not userInput: #skip blank lines
            continue

        words = userInput.split(maxsplit=2) #split at most 2 times
        CMD = words[0].upper() #stores what command user entered

        if CMD == SET and len(words) >= 3: #use upper so input is case insensitive, make sure there aren't too many arguements
            kvDatabase.setKeyValue(words[1], words[2])
        elif CMD == GET and len(words) >= 2:
            getResult = kvDatabase.getKeyValue(words[1])
            print(getResult)
        elif CMD == EXIT:
            break
        sys.stdout.flush() #sends output to gradebot immediately to ensure it receives response in time

if __name__ == "__main__":
    main()