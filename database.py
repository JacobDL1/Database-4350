import os #used for os.path.exists method that updates dbValues to have all entries data.db does
import sys #used for sys.stoud.flush(), addressed gradebot issue

file = "data.db" #used to reference data.db later

def loadDB(dbValues): #reads from data.db and takes any infromation present and uses it to rebuild the in-memory index (dbValues)
  if os.path.exists(file): #if data.db exists, each line is read, and the key value pair is appended to dbValues
    with open(file, "r") as f:
      for i in f:
        dbEntry = i.strip().split(" ", 2) #removes leading and trailing spaces, then splits the entry based on spaces, with a max of two splits

        if len(dbEntry) < 3: #skip empty or miswritten lines from gradebot
          continue
        duplicate = False #tracks if duplicate entry is found while importing data.db information into dbValues
        
        for j in dbValues: #compares key value of new line from data.db stored in dbEntry to those already in dbValues, ensuring that any duplicates from data.db are rooted out
          if j[0] == dbEntry[1]:
            j[1] = dbEntry[2]
            duplicate = True
            break
            
        if not duplicate:
          dbValues.append([dbEntry[1].strip(), dbEntry[2].strip()]) #dbEntry[0] is SET, so following key value pairs and index 1 and 2 is appended to dbValues

def setKeyValue(dbValues, key, value): #if the user types SET, stores following two terms as a key value pair in both dbValues and data.db
  duplicate = False
  for i in dbValues: #checks if new key is already present in dbValues, and updates key's value in dbValues if there is a duplicate
    if i[0] == key:
      i[1] = value
      duplicate = True
      break
      
  if not duplicate:
    dbValues.append([key, value])
    
  with open(file, "a") as f: #opens and writes to data.db
    f.write(f"SET {key} {value}\n")
    f.flush() #used for making sure SET is complete by the time GET is used for gradebot
    os.fsync(f.fileno()) #used for making sure SET is complete by the time GET is used for gradebot
  print("OK") #confirmation of SET command's success

def getKeyValue(dbValues, key): #if the user types GET, searched through dbValues for the user specified key and returns the corresponding value if the key is found
  foundValue = ""
  
  for i in dbValues: #comapres user-provided key to entries in dbValues, prints value if key is found
    if i[0] == key:
      foundValue = (i[1])
  if foundValue != "":
    print(foundValue)

def main(): #main loop for taking in user input and calling the necessary functions to respond
  dbValues = [] #stores all set command key value pairs for faster searching when using get
  loadDB(dbValues)
  
  while True: #continues looping until broken allowing for contuninous input
    try:
      userInput = input()
    except EOFError:
      break
      
    userInput = userInput.strip() #removes leading/trailing spaces for accurate indexing
    words = userInput.split(" ", 2) #splits userInput into its individual words, maxes out at two splits to make sure users can enter values that have spaces
    
    if words[0].upper() == "SET": #upper is used to make sure if people type any command in lowercase the program still recognizes the intent of the user
      setKeyValue(dbValues, words[1].strip(), words[2].strip())
    elif words[0].upper() == "GET":
      getKeyValue(dbValues, words[1].strip())
    elif words[0].upper() == "EXIT":
      break
      
    sys.stdout.flush()
          
if __name__ == "__main__":
  main()
