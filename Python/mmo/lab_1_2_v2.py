"""
Python интерпретатор проигнорирует этот блок текста, 
рассматривая его как строковой литерал, а не исполняемый код.
"""


input_string = input("Введите строку: ")
number = '' 
for char in input_string:
    if char.isdigit():
        number += char  

if number:
    print(number)