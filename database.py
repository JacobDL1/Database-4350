def main():
  file = "data.db" #used to reference data.db later
  dbValues = [] #stores all set command key value pairs for faster searching when using get
  
  
  while(True): #continues looping until broken allowing for contuninous input
    set = False #tracks if user typed set
    get = False #tracks if user typed get
    userInput = input()
    userInput = userInput.strip() #removes leading/trailing spaces for accurate indexing
    words = userInput.split() #splits userInput into its individual words
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
    
    if (set): #if  user used SET, key value pair is appended to dbValues and written to data.db
      key = words[1]
      value = words[2]
      dbValues.append([key, value])
      
      with open(file, "a") as f: #opens and writes to data.db
        f.write(f"SET {key} {value}\n")
    elif (get): #if user used GET, key is searched for in dbValues and returned if found
      key = words[1]
      for i in dbValues:
        if i == key:
          print(i[1])
      print("No such value found in database")
          

if __name__ == "__main__":
  main()
