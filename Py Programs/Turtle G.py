import turtle

t = turtle

f = int(input("Enter Distance Of Lines In Pattern : "))
turn = float(input("Enter Degrees To Turn : "))
times = int(input("Enter Times To Do Pattern : "))

t.forward(100)

while times >= 1:
    t.left(turn)
    t.forward(f)