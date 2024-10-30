#functions and structures

def greet(name =  'Прекрасный человек'):
    print(f'Привет, {name}!')

def num_of_people_in_brsm(sum = 1000000000):
    sum *= 100
    return sum, 'ДОхера' 
greet()
print('Вернее...')
greet('Корней')

#Возврат количества человек в БРСМ
num, description = num_of_people_in_brsm(100)
print(f"Количество  человек в БРСМ составляет {num}({description})")

# Пример использования списков 
numbers = [1,2,3,4,5,6]
print(numbers[0])
print(numbers[-1])
numbers.append(8)
numbers.remove(4)
numbers.append(4)
print(numbers)
numbers.sort()
print(numbers)
numbers.reverse()
print(numbers)
numbers