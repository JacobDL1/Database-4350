import os #used for os.path.exists method that updates dbValues to have all entries data.db does

def main():
  file = "data.db" #used to reference data.db later
  dbValues = [] #stores all set command key value pairs for faster searching when using get

  if os.path.exists(file): #if data.db exists, each line is read, and the key value pair is appended to dbValues
    with open(file, "r") as f:
      for i in f:
        dbEntry = i.strip().split(" ", 2) #removes leading and trailing spaces, then splits the entry based on spaces, with a max of two splits
        dbValues.append([dbEntry[1], dbEntry[2]]) #dbEntry[0] is SET, so following key value pairs and index 1 and 2 is appended to dbValues
  
  while(True): #continues looping until broken allowing for contuninous input
    set = False #tracks if user typed set
    get = False #tracks if user typed get
    userInput = input()
    userInput = userInput.strip() #removes leading/trailing spaces for accurate indexing
    words = userInput.split(" ", 2) #splits userInput into its individual words, maxes out at two splits to make sure users can enter values that have spaces
    
    if words[0] == "SET":
      set = True
    elif words[0] == "GET":
      get = True
    elif words[0] == "EXIT":
      print("Exiting")
      break;
    else:
      print("Invalid command entered")
      
    key = ""
    value = ""
    duplicate = False #used to track if a SET request's key already exists
    
    if (set): #if  user used SET, key value pair is appended to dbValues and written to data.db, and if key is a duplicate, existing key has its value changed to new SET request's value
      key = words[1]
      value = words[2]
      
      for i in dbValues:
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
      foundValue = "";
      
      for i in dbValues:
        if i[0] == key:
          foundValue = (i[1])
      if foundValue == "":
        print("No such value found in database")
      else:
        print(foundValue)
          

if __name__ == "__main__":
  main()
