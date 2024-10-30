def a():
    print('Start of a()')
    b() #Вызов b()

def b():
    print('Start of b()')
    c() #вызов c()

def c():
    print('Start of c()')
    42/0 #Порождает ошибку деления на нуль.

try:
    a() #Вызов a()
except c: ZeroDivisionError
print('You are stuped')
