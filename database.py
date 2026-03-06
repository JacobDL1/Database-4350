def main():
  file = "data.db" #used to reference data.db later
  
  
  while(true): #continues looping until broken allowing for contuninous input
    set = false #tracks if user typed set
    get = false #tracks if user typed get
    userInput = input()
    userInput = userInput.strip() #removes leading/trailing spaces for accurate indexing
    if userInput[0] == "SET":
      set = true
    elif userInput[0] == "GET":
      get = true
    elif userInput[0] == "EXIT":
      print(exiting)
      break;
    else:
      print("Invalid command entered")
      
    dbValues = [] #stores all set command key value pairs for faster searching when using get
    key = ""
    value = ""
    
    if (set): #if  user used SET, key value pair is appended to dbValues and written to data.db
      userInput[1] = key
      userInput[2] = value
      dbValues.append([key, value])
      
      with open(DB_FILE, "a") as f: #opens and writes to data.db
        f.write(f"SET {key} {value}\n")
    elif (get): #if user used GET, key is searched for in dbValues and returned if found
      userInput[1] = key
      for i in dbValues:
        if i == key:
          return i[1]
      return "No such value found in database"
          

if __name__ == "__main__":
  main()
