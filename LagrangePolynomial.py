
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

path_file = "/content/DataPrV9.csv" # Задаём путь к файлу
delim = "," # Указываем разделитель
x_title = "Время" # Задаём заголовок оси x
y_title = "Цена за 1 кв.м." # Задаём заголовок оси y
graphic_title = "Динамика изменения стоимости жилья на первичном рынке (Россия)" # Задаём заголовок графику
number_point = 300  # Указываем количество точек для рисования функции в диапазоне интерполяции. Влияет на сглаженность линии.
range_start = 0 # Указываем начало диапазона интерполяции
range_number = 15 # Указываем количество точек для интерполяции
extension_left = 0.06    # Задаём значение в %, на которое будет увеличен интервал рисования графика функции Лагранжа справа от последней точки интерполяции
extension_right = 0.01   # Задаём значение в %, на которое будет увеличен интервал рисования графика функции Лагранжа слева от первой точки интерполяции 

data = np.genfromtxt(path_file, delimiter=delim, dtype= None, encoding = 'utf-8') # читаем данные
data_divided_time = []  # Создаём массив для хранения даты: года, месяца и дня
y = [] # Создаём массив для хранения значений по оси y
data_time = [] # Создаём массив для хранения даты типа datetime
x = [] # Создаём массив для хранения количества секунд, прошедших с начала первой даты в массиве

def lagran(f_x):   # функция, реализующая вычисление в заданной точке по оси х значения y
  accumulation = 0.0         # Накапливаем сумму всех слагаемых 
  for i in range(len(x)):
    multiplication = 1.0     # Записываем значение всех умноженных скобок в рамках одного слагаемого
    for ii in range(len(x)):
      if ii != i:
        multiplication = multiplication*(f_x - x[ii]) / (x[i] - x[ii])
    accumulation = accumulation + multiplication*y[i]
  return accumulation

try:
    for i in range(range_start,range_start+range_number):   # наполняем массивы данными
         data_divided_time.append(data[i][0].split('.'))
         y.append(data[i][1])
         data_time.append(dt.datetime( int(data_divided_time[i-range_start][2]),int(data_divided_time[i-range_start][1]), int(data_divided_time[i-range_start][0]) ))
         x.append(  (data_time[i-range_start] - dt.datetime(1970, 1,1)  ).total_seconds()     )

    array_x = np.linspace(x[0]*(1 - (extension_left/100)), x[range_number-1]*(1 + (extension_right/100)),number_point) 
    array_y = [lagran(i) for i in array_x]

    array_x_datetime = [] # Создаём массив для хранения значений, который подставляются в формулу Лагранжа по оси y типа данных datetime

    for i in array_x:
      array_x_datetime.append( dt.datetime.utcfromtimestamp(int(i))  ) # заполняем массив данными, исходя из времени, прошедшем с начала 1970 года

    plt.figure(figsize = (20,10)) # Задаём размеры прорисовки окна
    plt.xlabel(x_title, fontsize=16)
    plt.ylabel(y_title, fontsize=16)
    plt.title(label = graphic_title, fontsize = 18)
    plt.scatter(data_time, y, c = 'deeppink', s = 200)  # Рисуем исходные точки. Параметр s контролирует размер точек.
    plt.grid() # Рисуем сетку
    plt.plot(array_x_datetime, array_y , linewidth = 2) # Рисуем график получившейся функции
    plt.show() # Показываем график

except IndexError:
  print('Введите верный диазпаон интерполируемых точек или проверьте правильность входного набора данных в файле')
  exit()