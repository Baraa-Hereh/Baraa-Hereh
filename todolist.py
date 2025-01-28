import sqlite3
from datetime import datetime
date_format = "%d-%m-%Y"
try:
    db = sqlite3.connect("ToDoList.db")
    cr = db.cursor()
    cr.execute("create table if not exists tasks(name text ,date text ,state text )")
except sqlite3.Error as er:
    print(f"Error Reading Data{er}")
messge = """ 
What Do You Want To Do ?
 "a" => Addition A Tasks 
 "s" => Show Daily Tasks
 "u" => Update Daily Tasks
 "d" => Delete Daily Tasks 
 "m" => Mark Completion  
  """
def commit_and_close():
    db.commit()
    db.close()

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date frmat. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)
    

def add_tasks():

    try:
        name = input("Write Taske  name : ").strip().lower()
    except ValueError:
        print("Pleas Enter Name Like (study) ")
    state = " "
    ma = "Enter the date of the task (dd-mm-yyyy) or enter for today's date:) "
    date = get_date(ma,allow_default=True)
    result=sesrch_for_data(name,date)
    if result:
        print("this task is alwrdy exists :)")
    else:
        cr.execute("insert into tasks values(?,?,?) ",(name,date,state))
        commit_and_close()
        print(" Added Successfully..")

def sesrch_for_data(name,date):
    cr.execute(f"Select * from tasks where name = '{name}'and date = '{date}'")
    result = cr.fetchone()
    return result

def delet_tasks():

    name = input("Write The Name Of The Tasd You Wnant To Delete : ").strip().lower()
    ma = "Enter the date of  the task  you want to delete or press enter for today's date :)  "
    date = get_date(ma,allow_default=True)
    result = sesrch_for_data(name,date)
    if result:
        cr.execute(f"Delete from tasks where name ='{name}' and  date = '{date}'")
        commit_and_close()
        print("Delete Successfully")
    else:
        print("Sorry this task doesn't exist")

def update_task():

    ta = input(" Enter the name of the task you want to edit :  ").strip().lower()
    m = " Enter the date of the task you wnat to edit or prees  inter for today's date  "
    da = get_date(m,allow_default=True)
    result = sesrch_for_data(ta,da)
    if result:
        optioin = input ("""What do you want to change name or date
                          enter 'name' for name and 'date' for date 
                          enter 'together' for name and date
                            enter 'q' for exit  : """).strip().lower()
        if optioin == "name":
            new_tk = input("Enter your new task name : ").strip().lower()
            cr.execute(f"update  tasks set name = '{new_tk}' where name = '{ta}' and  date = '{da}'")
            print("Successfully modified.. ")
            commit_and_close()
        elif optioin == "date":
            new_da = get_date ("Enter your new task date : ",allow_default=True)
            cr.execute(f"update tasks set date = '{new_da}'where name = '{ta}' and date ='{da}'")
            print("Successfully modified.. ")
            commit_and_close()
        elif optioin == "together":
            new_tk = input("Enter your new task name : ").strip().lower()
            new_da = get_date("Enter your new task date or press enter for today's date : ",allow_default=True)
            cr.execute(f"UPDATE tasks SET name = '{new_tk}', date = '{new_da}' WHERE name = '{ta}' AND date = '{da}'")
            print("Successfully modified.. ")
            commit_and_close()
        elif optioin == "Q":
            print(" EXIT....")
    else:
        print("Sorry this task  doesn't found")

def mark():
    while True:
        taks_name = input(" Enter the name of the completed task or press enter to break  : ").strip().lower()
        
        if taks_name != "":
            task_date = get_date(" Enter the date of the completed task : ",allow_default=True)
            result =sesrch_for_data(taks_name,task_date)
            if result:
                cr.execute(f"Update tasks set state = 'done' where name = '{taks_name}' and date = '{task_date}'")
                commit_and_close()
                print("Successfully Modified..")
            else:
                print("Sorry this task doesn't exist")
        else:
            print("Done...")
            break

def show_task():
    op = input(""" Do you want to show all the tasks or tasks of this dat 
                    'all' => all tasks : 
                    'today' => Today's Tasks : """).strip().lower()
    if op == "all":
        cr.execute(f"select * from tasks")
        all_taks = cr.fetchall()
        print(" ..... All Tasks .....")
        for row in all_taks:
            print(f" Name : {row[0]}   Date : {row[1]} State : {row[2]} ")
    elif op == "today":
        date = get_date(" Enter the date or prees  inter for today's date ",allow_default=True )
        cr.execute(f"select * from tasks where  date='{date}'")
        result = cr.fetchall()
        if result:
            print("Tasks to be accomplished ")
            for row in result:
                print(f" Name : {row[0]}   Date : {row[1]} State : {row[2]} ")
        else:
            print("There are no tasks on this day. ")
    else:
        print(" EXIT....")

    
if __name__ == "__main__":
    o = input(messge).strip().lower()  
    if o == "a":
        add_tasks()
    elif o == "s":
        show_task()
    elif o == "m":
        mark()
    elif o == "u":
        update_task()
    elif o == "d":
        delet_tasks()   
    else:
        print("Invlaid vlaue ")   
        


