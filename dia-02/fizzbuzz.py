"""FizzBuzz: de 1 a 100, mostra Fizz, Buzz, FizzBuzz ou o próprio número."""

for numero in range(1, 101):
    if numero % 15 == 0:
        print("FizzBuzz")
    elif numero % 3 == 0:
        print("Fizz")
    elif numero % 5 == 0:
        print("Buzz")
    else:
        print(numero)