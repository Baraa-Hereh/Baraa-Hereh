import json

with open ("contacts.json","r")as f:

    people =json.load(f)["contacts"]
    
print("Hi ,welcom to the contact Managament Sustem:")
print()

def add_person():  
    name = input ("Name: ")
    age = input ("Age:")
    email = input("Email:")
 
    person = {"name":name,"age":age,"email":email}
    return person

def displat_people (people):
    for i , person in enumerate(people):
        print(i+1,"-",person["name"],"|",person["age"],"|",person["email"])

def delet_contcat (person):
    displat_people(people)
    while True:
        number = input("Enter  a number to delete:")
        try:
            number= int (number)
            if number<=0 or number>len(people):
                print("Invalid number,out of range.")
            else:
                break
        except:
            print("Invalid number ")
    people.pop(number - 1)
    print("Person deleted.")

def search(people):
    search_name = input("Search for a name: ").lower()
    results=[]
    for person in people:
        name = str(person["name"])
        if search_name in name.lower():
            results.append(person)
    displat_people(results)
while True:
    print()
    print("contact list size :",len(people))
    command = input("you can 'add','Delete' or 'Search' and 'Q' for quit: ").lower()
    if command =="add": 
        person = add_person()
        people.append(person)
        print("Person added !")
    elif command == "delete":
        delet_contcat(people)
    elif command == "search":
        search(people)
    elif command == "q":
        break
    else:
        print("Enavalid command.")
with open ("contacts.json","w")as f:
    json.dump({"contacts":people},f)