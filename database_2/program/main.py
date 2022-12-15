import math
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt


def Erlang_1(A, V):
    result = [1, A / (1 + A)]
    for i in range(2, V + 1):
        result.append(A * result[i - 1] / (V + A * result[i - 1]))
    return result[V]


# task 1.2
count = 5000
a = np.linspace(0, count, count + 1, dtype=int)
f = Erlang_1(a, 170)

plt.plot(a, f)
plt.xlabel('Интенсивность поступающей нагрузки (A), вызовы')
plt.ylabel('Вероятность блокировки заявок (Р)')
plt.legend(['V = 170'])
plt.grid()
plt.show()

# task 1.3
A = 85
count = 100
v = np.linspace(0, count, count + 1, dtype=int)
f = list()
for i in v:
    f.append(Erlang_1(A, i))

plt.plot(v, f)
plt.xlabel('Число обслуживающих устройств (V), шт')
plt.ylabel('Вероятность блокировки заявок (Р)')
plt.legend(['A = 85'])
plt.grid()
plt.show()


def Erlang_2(A, V):
    return Erlang_1(A, V) / (1 - A / V * (1 - Erlang_1(A, V)))


def AvgLength(A, V):
    return A * Erlang_1(A, V) / ((V - A) + A * Erlang_1(A, V)) * V / (V - A)

'''
# task 2.2
count = 170
a = np.linspace(160, count, 1000)  # интенсивность поступающей нагрузки
f = Erlang_2(a, 170)

plt.plot(a, f)
plt.xlabel('Интенсивность поступающей нагрузки (A), вызовы')
plt.ylabel('Вероятность ожидания начала обслуживания (Р)')
plt.legend(['V = 170'])
plt.grid()
plt.show()

v = 170
a = np.linspace(160, v - 1, 1000)
f = AvgLength(a, v)
plt.plot(a, f)
plt.xlabel('Интенсивность поступающей нагрузки (A), вызовы')
plt.ylabel('Средняя длина очереди, шт')
plt.legend(['V = 170'])
plt.grid()
plt.show()

# task 2.3

A = 85
count = 95
v = np.linspace(85, count, dtype=int)
f = list()
for i in v:
    f.append(Erlang_2(A, i))

plt.plot(v, f)
plt.xlabel('Число обслуживающих устройств (V), шт')
plt.ylabel('Вероятность ожидания начала обслуживания (Р)')
plt.legend(['A = 85'])
plt.grid()
plt.show()

A = 85
count = 95
v = np.linspace(A + 1, count, dtype=int)
avg = list()
for i in v:
    avg.append(AvgLength(A, i))

plt.plot(v, avg)
plt.xlabel('Число обслуживающих устройств (V), шт')
plt.ylabel('Средняя длина очереди, шт')
plt.legend(['A = 85'])
plt.grid()
plt.show()
'''