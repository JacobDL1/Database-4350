import os #used for os.path.exists method that updates dbValues to have all entries data.db does
import sys #used for sys.stoud.flush(), addressed gradebot issue

file = "data.db" #used to reference data.db later

def loadDB(dbValues):
    """reads from data.db and takes any infromation present and uses it to rebuild the in-memory index (dbValues)"""
    if os.path.exists(file): #if data.db exists, each line is read, and the key value pair is appended to dbValues
        with open(file, "r", encoding="utf-8") as f: #opens using utf-8 encoding to parse file properly
            for i in f:
                dbEntry = i.strip().replace('\r', '').split(maxsplit=2) #removes leading and trailing spaces, then splits the entry based on spaces, with a max of two splits, use decode on i to make python accurately interpret text for compatibility with the grader
                if len(dbEntry) < 3 or dbEntry[0] != "SET": #skip empty or miswritten lines from gradebot
                    continue
                key = dbEntry[1]
                value = dbEntry[2]
                duplicateCheck(dbValues, key, value)

def duplicateCheck(dbValues, key, value):
    """Updates key's value if there is a duplicate key in dbValues, if there is no duplication, key-value pair is appended"""
    for i in dbValues: #compares key value of new line from data.db stored in dbEntry to those already in dbValues, ensuring that any duplicates from data.db are rooted out
        if i[0] == key:
            i[1] = value
            return
    dbValues.append([key, value])

def setKeyValue(dbValues, key, value):
    """if the user types SET, stores following two terms as a key value pair in both dbValues and data.db"""
    duplicateCheck(dbValues, key, value)
    with open(file, "a", encoding="utf-8") as f: #opens and writes to data.db, opens using utf-8 encoding to parse file properly
        f.write(f"SET {key} {value}\n")
        f.flush() #used for making sure SET is complete by the time GET is used for gradebot
        os.fsync(f.fileno()) #used for making sure SET is complete by the time GET is used for gradebot

def getKeyValue(dbValues, key):
    """compares user-dictated key against the keys in dbValues, clears and reloads dbValues right before checking to ensure all entries are present"""
    dbValues.clear()
    loadDB(dbValues)
    for i in dbValues: #comapres user-provided key to entries in currValues, prints value if key is found, used because relying on dbValues created errors with grader
        if i[0] == key:
            print(i[1])
            sys.stdout.flush()
            return
    print("")
    sys.stdout.flush()

def main():
    """main loop for taking in user input and calling the necessary functions to respond"""
    dbValues = [] #stores all set command key value pairs for faster searching when using get
    loadDB(dbValues)
    while True: #continues looping until broken allowing for contuninous input
        try:
            userInput = input().strip().replace('\r', '') #removes leading and trailing whitespace, and deletes any \r
        except EOFError:
            break

        if not userInput: #skips blank lines
            continue
        words = userInput.split(maxsplit=2) #splits userInput into its individual words, maxes out at two splits to make sure users can enter values that have spaces
        if words[0].upper() == "SET" and len(words) >=3: #upper makes user input case insensitive, words is at least 3 words because that covers the command, key, and the value, where the value can include its own spaces
            setKeyValue(dbValues, words[1], words[2])
        elif words[0].upper() == "GET" and len(words) >=2: #at least 2 since there needs to be the command and the key
            getKeyValue(dbValues, words[1])
        elif words[0].upper() == "EXIT":
            break
        sys.stdout.flush()
                    
if __name__ == "__main__":
    main()
