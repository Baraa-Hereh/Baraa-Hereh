
"""
this program will assist in the operation of shops as this program will 
perform many tasds such as calcualting zakat and calculating goods
prices for the exchange rate
"""
import csv



def csv_open(file_name,mode="r"):
      """Open CSV file with the given mode."""
      return open(file_name,mode,newline="")
def insert_goods_to_file(goods_name:str,amount:int,price_dollar:float,price_sy:float)->None:
         """Store the name, quantity, price in dollars and price in Syrian lira."""
         goods=[]
         with csv_open("repository.csv") as file:
            reader = csv.reader(file)
            header = next(reader)
            goods = list(reader)
      

         found = False  
         for row in goods:
            if row and goods_name == row[0]:
                row[1] = str(float(row[1]) + amount)  
                found = True
                break

         with csv_open("repository.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)  
            writer.writerows(goods)

         if not found:
            with csv_open("repository.csv", "a") as file:
                writer = csv.writer(file)       
                writer.writerow([goods_name, amount, price_dollar, price_sy])

        


def input_goods()->tuple:
    """  this function enters information from the user """

    goods_name = str( input("Enter the name of goods :"))
    amount = float(input("Enter  amount : "))
    price_dollar = float(input("Enter the price of goods in dollars : "))
    price_sy = float(input("Enter the price of goods in sy  : "))
    return goods_name,amount,price_dollar,price_sy

def search_for_goods(target_name):

    """Search for goods."""

    with csv_open("repository.csv","r") as file :
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if target_name in row :
                return row 
        return None

def insert_target_name() :
    """ this function insert the target name """ 
    target_name  = str(input("Enter the name of goods : "))
    return target_name  

 

def print_goods_info(name, amount, price_dollar, price_sy) -> None:
    """Print information about goods."""
    print(f"Name: {name}\nAmount: {amount}\nPrice in $: {price_dollar}\nPrice in SY: {price_sy}")

def insert_goods_from_input():
    """get user input and save goods info in file"""
    goods_name,amount,price_dollar,price_sy = input_goods()
    return insert_goods_to_file(goods_name,amount,price_dollar,price_sy)

def search_goods_form_input()->None:
    """Get target name from user and serarch for goods then print info"""
    target_name = insert_target_name()    
    row = search_for_goods(target_name)
    if row is None:
        print("the goods is not found")
    else:
        name = row[0]
        amount  =  row [1]
        price_dollar = row[2]
        price_sy = row [3]
        print_goods_info(name,amount,price_dollar,price_sy)


def input_dollar():
    """
    input dollar form user
    """
    dollar = int(input("Enter the price dollar: "))
    return dollar

def price_change_for_dollar()->None:
    """
    change price the goods by dollar 
    """
    dollar = input_dollar()
    
    with csv_open("repository.csv", "r") as file:
        reader = csv.reader(file)
        price = list(reader)
    
    for row in price[1:]:
        row[3] = str(float(row[2]) * dollar)      
    with csv_open("repository.csv", "w" ) as file:
        writer = csv.writer(file)
        writer.writerows(price)

def zakah()->None:
    with csv_open("repository.csv","r") as file:
       reader = csv.reader(file)
       header = next (reader)
       total_sum =0 
       for row in reader:
         total_sum += float(row[1]) * float(row[3])  
            
       zakah = (total_sum - (0.01 * total_sum)) * 0.025
       print(f"the value of zakah is {zakah}")
def insert_goods_into_the_invoice()->None:
    """"
    tis function will write an invoice for the goods sold
    
     """
    name_list = []
    amount_list = []
    price_list = []
    while True:
        name = input("Enter the name of goods : ")
        if name == "" :
            break
        else:
            try:
                amount= float(input("Enter the amount : "))
            except ValueError:
                 print("Please enter a valid number for amount.")
                 break
        name_list.append(name)
        amount_list.append(amount)
        with csv_open("repository.csv","r") as file :
            reader= csv.reader(file)
            header= next(reader)
            goods = list (reader)
        for row in goods:
                if row [0]==name:
                    price = str( float(amount)  * float(row[3]))
                    new_amount = str  (float(row[1]) - float(amount))
                    row[1]= new_amount
                    price_list.append(price)
        with csv_open("repository.csv","w")as file :
                     writer = csv.writer(file)
                     writer.writerow(header)
                     writer.writerows(goods)        
    for i in range(len(name_list)):
        print(f"goods name: {name_list[i]}, amount: {amount_list[i]}, price: {price_list[i]}")
    sum = 0 
    for i in range(len(price_list)) :
         sum += float(price_list[i])
    print(f"     the final total is  : {sum}    ")
           
option = input("""chois the opertion :
if you want to insert goods press insert :
if you want to search for goods press search:
if you wnat to change the price press  dollar :
if you want to calculate zakah press zakah : 
if you want to calculate invoice press invoice : 
                """).strip()
if option == "insert" :
    insert_goods_from_input()
elif option == "search" :
    search_goods_form_input()
elif option == "dollar" :
    price_change_for_dollar()
elif option == "zakah":
    zakah()
elif option == "invoice":
    insert_goods_into_the_invoice()
else:
    print(" input values are incorrect  ")