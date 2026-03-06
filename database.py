import os #used for os.path.exists method that updates dbValues to have all entries data.db does
import sys #used for sys.stoud.flush(), addressed gradebot issue

def main():
  file = "data.db" #used to reference data.db later
  dbValues = [] #stores all set command key value pairs for faster searching when using get

  if os.path.exists(file): #if data.db exists, each line is read, and the key value pair is appended to dbValues
    with open(file, "r") as f:
      for i in f:
        dbEntry = i.strip().split(" ", 2) #removes leading and trailing spaces, then splits the entry based on spaces, with a max of two splits
        importDuplicate = False #tracks if duplicate entry is found while importing data.db information into dbValues

        for j in dbValues: #compares key value of new line from data.db stored in dbEntry to those already in dbValues, ensuring that any duplicates from data.db are rooted out
          if j[0] == dbEntry[1]:
            j[1] = dbEntry[2]
            importDuplicate = True
            break
            
        if not importDuplicate:
          dbValues.append([dbEntry[1], dbEntry[2]]) #dbEntry[0] is SET, so following key value pairs and index 1 and 2 is appended to dbValues
  
  while(True): #continues looping until broken allowing for contuninous input
    set = False #tracks if user typed set
    get = False #tracks if user typed get
    try:
      userInput = input()
    except EOFError:
      break
    userInput = userInput.strip() #removes leading/trailing spaces for accurate indexing
    words = userInput.split(" ", 2) #splits userInput into its individual words, maxes out at two splits to make sure users can enter values that have spaces
    
    if words[0].upper() == "SET": #upper is used to make sure if people type any command in lowercase the program still recognizes the intent of the user
      set = True
    elif words[0].upper() == "GET":
      get = True
    elif words[0].upper() == "EXIT":
      break
    else:
      print("Invalid command entered")
      
    key = ""
    value = ""
    duplicate = False #used to track if a SET request's key already exists
    
    if (set): #if  user used SET, key value pair is appended to dbValues and written to data.db, and if key is a duplicate, existing key has its value changed to new SET request's value
      key = words[1]
      value = words[2]
      
      for i in dbValues: #checks if new key is already present in dbValues, and updates key's value in dbValues if there is a duplicate
        if i[0] == key:
          i[1] = value
          duplicate = True
          break
          
      if not duplicate:
        dbValues.append([key, value])
      
      with open(file, "a") as f: #opens and writes to data.db
        f.write(f"SET {key} {value}\n")
    
    elif (get): #if user used GET, key is searched for in dbValues and returned if found
      key = words[1]
      foundValue = ""
      
      for i in dbValues: #comapres user-provided key to entries in dbValues, prints value if key is found
        if i[0] == key:
          foundValue = (i[1])
      if foundValue != "":
        print(foundValue)

        
    sys.stdout.flush()
          

if __name__ == "__main__":
  main()
