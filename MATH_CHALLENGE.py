import random
import time
OPERATORS=["+","-","*"]
print("Enter the range of number ! ")
MIN_OPERAND = int(input("Enter the min number : "))
MAX_OPERAND= int(input ("Enter the max number : "))
TOTAL_PROBLEMS = int (input("Enter the number of problems : "))

def gernerate_problec():
    left = random.randint(MIN_OPERAND,MAX_OPERAND)
    right = random.randint(MIN_OPERAND,MAX_OPERAND)
    operator = random.choice(OPERATORS)
    expr = str(left )+" "+operator+" "+str(right)
    answer = eval(expr)
    return expr,answer

wrong =0
input("Press enter to start !")
print("----------------------")
count = 0
start_time = time.time()
for i in range(TOTAL_PROBLEMS):
    expr , answer = gernerate_problec()
    while True:
        guess = input("Problem # "+str(i+1)+": "+ expr +" = ")
        if guess == str(round(answer,1)):
            count = 0
            break
        else :
            count+=1
            if count == 3 :
                print(f"the answer is {answer} pleas go to the next problem ")
                count = 0
                break
        wrong +=1
end_time = time.time()
total_time = round(end_time - start_time,2)
print("------------------")
if wrong <= 2 :
    print("your level is very good ! ")
elif 2 < wrong < 4 :
    print("your level is not bad ! ")
elif wrong > 4 :
    print("you are  very bad in math!") 
print("Nice work! you finished in",total_time,"seconds")

