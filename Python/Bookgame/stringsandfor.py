#range(1,6) от 1 до  5

for i in range(1,6):
  print(i)
  #list- создание списка
numbers = list(range(1,6))
print(numbers)
even_numbers = list(range(2,11,2))#for(i<11;i+=2)
print(even_numbers)
squares = []
for value in range(1,11):#for(i=1; i<11; i++)
  square = value**3
  squares.append(square)
print(squares)