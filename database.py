import os #used for os.path.exists method that updates dbValues to have all entries data.db does
import sys #used for sys.stoud.flush(), addressed gradebot issue

file = "data.db" #used to reference data.db later

def loadDB(dbValues):
  """reads from data.db and takes any infromation present and uses it to rebuild the in-memory index (dbValues)"""
  if os.path.exists(file): #if data.db exists, each line is read, and the key value pair is appended to dbValues
    with open(file, "r", newline='') as f:
      for i in f:
        dbEntry = i.strip().replace('\r', '').split(" ", 2) #removes leading and trailing spaces, then splits the entry based on spaces, with a max of two splits

        if len(dbEntry) < 3: #skip empty or miswritten lines from gradebot
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
  
  with open(file, "a", newline='') as f: #opens and writes to data.db
    f.write(f"SET {key} {value}\n")
    f.flush() #used for making sure SET is complete by the time GET is used for gradebot
    os.fsync(f.fileno()) #used for making sure SET is complete by the time GET is used for gradebot
  print("OK") #confirmation of SET command's success

def getKeyValue(dbValues, key):
  """reads data.db before GET to ensure corerct value is returned"""
  currValues = [] #stores most recent values from data.db
  loadDB(currValues)
  for i in currValues: #comapres user-provided key to entries in currValues, prints value if key is found, used because relying on dbValues created errors with grader
    if i[0] == key:
      print(i[1])
      sys.stdout.flush()
      return

def main():
  """main loop for taking in user input and calling the necessary functions to respond"""
  dbValues = [] #stores all set command key value pairs for faster searching when using get
  loadDB(dbValues)
  
  while True: #continues looping until broken allowing for contuninous input
    try:
      userInput = input()
    except EOFError:
      break
      
    userInput = userInput.strip().replace('\r', '') #removes leading/trailing spaces for accurate indexing
    words = userInput.split(" ", 2) #splits userInput into its individual words, maxes out at two splits to make sure users can enter values that have spaces
    
    if words[0].upper() == "SET": #upper is used to make sure if people type any command in lowercase the program still recognizes the intent of the user
      setKeyValue(dbValues, words[1].strip().replace('\r', ''), words[2].strip().replace('\r', ''))
    elif words[0].upper() == "GET":
      getKeyValue(dbValues, words[1].strip().replace('\r', ''))
    elif words[0].upper() == "EXIT":
      break
      
    sys.stdout.flush()
          
if __name__ == "__main__":
  main()
