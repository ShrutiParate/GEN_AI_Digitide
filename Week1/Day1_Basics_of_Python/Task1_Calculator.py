print("CALCULATOR")

print("1- Addition")
print("2- Subtraction")
print("3- Multiplication")
print("4- Division")

operation= int(input("Choose the operation from 1-4: "))


if operation in [1,2,3,4]:
    num1= int(input("Enter the number 1: "))
    num2= int(input("Enter the number 2: "))

if operation==1:
    result = num1 + num2
elif operation==2:
    result = num1 - num2
elif operation==3:
    result = num1 * num2
elif operation==4:
    result = num1 / num2
else:
    print("Invalid operation entered.")

print(" The result of the operation is {}".format(result))






