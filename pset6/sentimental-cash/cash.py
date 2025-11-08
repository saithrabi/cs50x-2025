from cs50 import get_float
while True:
    change = get_float("Change: ")
    if (change > 0):
        break

totalcents = int(change * 100)

quarters = int(totalcents / 25)
totalcents -= quarters * 25

dimes = int(totalcents / 10)
totalcents -= dimes * 10

nickels = int(totalcents / 5)
totalcents -= nickels * 5

pennies = totalcents

totalcoins = quarters + dimes + nickels + pennies

print(totalcoins)
