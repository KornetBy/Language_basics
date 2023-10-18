bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles[0].title())
message = bicycles[0].title() +" " + bicycles[-1].title()
print(message)
print(bicycles[0].title(),bicycles[-1].title())
bicycles[0] = "sydr"
print(bicycles[0])
ghjcnj = "fignya"
bicycles.append(ghjcnj)
print(bicycles)
ghjcnjnf='bom'
bicycles.insert(2,ghjcnjnf)
print(bicycles)
del bicycles[3]
print(bicycles)
bicycles.pop()
print(bicycles)
#pop(8,////)-достаёт 9 элемент из списка, можно поместить в переменную(без цифры берётся последний)(можно указать переменную, в которую записано слово)
#insert-противоположноть pop, вставляет в нужное место элемент(можно указать переменную, в которую записано слово)
#del удаляет полность элемент с номером из списка
#append - добавляет в конец списка(можно указать переменную, в которую записано слово)
#remove - удаляет элемент по имени(можно указать переменную, в которую записано слово)(удаляет только первое вхождение слова)
bicycles.remove('bom')
print(bicycles)
#sort - сортирует по возростанию список, причем изменяет весь список. Для определения в опратном порядке use reverse=True
#Нельзя написать сразу в принте
bicycles.sort()
print(bicycles)
#sorted - применяется для временной сортировки, которая не сохраняется в списке. reverse=True как и для sort(идёт после списка)
print(sorted(bicycles, reverse = True))
#reverse - вывод списка в обратном порядке с сохранением его. 
bicycles.reverse()
print(bicycles)
print(sorted(bicycles))
#len() - длина списка
