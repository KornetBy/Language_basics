import math, random     
from decimal import Decimal
from fractions import Fraction
print(math.pi, math.pi)
print('-------------------------')
print(math.sqrt(9))
s = 'zamer'
print(s[-0])
print(s[1:])
s = '-'
print(s*10)
s = 'koker'
s = 'j' + s[1:]
print(s)
print(4 << 2)
print(math.trunc(-4.9), math.floor(-4.9), round(-4.9))
print(2+1j*3)
print(0b100 == 4)
print(0xF == 15)
print(0o10 == 8, oct(64), hex(64), bin(64))
print(eval('64'))
print(eval('0x40'))
print(4 | 2)
print(4 & 5)
x= 99 
print(bin(x), x.bit_length())
print(pow(2, 4))
print(abs(-42))
print(min(2,10,8,7), max(18,103,1,0))
#random.choice()
#random.randint()
print(Decimal('0.1')+Decimal('0.1')+Decimal('0.1')-Decimal('0.3'))
x = Fraction(1, 3)
print(x)

