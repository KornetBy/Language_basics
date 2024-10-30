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


message = 'hello python world!'
print('Simple print: '+ message)
print('Method "title": '+ message.title())
print('Method "upper": '+ message.upper())
print('Method "capitalize": '+ message.capitalize())
print('Method "lower": '+ message.lower())