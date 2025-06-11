## ВКР на тему "Разработка мобильного робота для выполнения логистических операций"


[Презентация](https://github.com/CepbluKot/diploma/blob/master/%D0%9F%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F.pdf) </br>
[Отчет](https://github.com/CepbluKot/diploma/blob/master/%D0%9E%D1%82%D1%87%D0%B5%D1%82.pdf) </br>


## Состав ПО решения
mcu_modules - ПО, запускаемое на аппаратном обеспечении (микроконтролерах ATmega328P)</br>
operator_modules - ПО, запускаемое на стороне оператора</br>
robot_modules - ПО, запускаемое на стороне робота</br>
data_formats - форматы даных для обмена информацией</br>


## Сборка решения
Проект работает на ОС Linux Ubuntu 22.04 </br>
Для сборки нужен Python 3.8 </br>

```
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.8
```

Перед сборкой необходимо установить libfreenect (собирать под python 3.8): https://github.com/alwynmathew/libfreenect-with-python </br>


Для корректной работы проекта требуется подключение модулей аппаратного обеспечения</br>
Материалы по сборке элементов аппаратного обеспечения представлены в приложениях отчета, доступного по указанной выше ссылке</br>


Запуск:
```
python3.8 -m pip install -r requirements.txt
python3.8 launch_operator_part.py
python3.8 launch_robot_part.py
```

Сборка ПО для микроконтроллеров выполнялась при помощи https://platformio.org/ </br>
Для сборки ПО для микроконтроллеров применяются библиотеки:  </br>
https://github.com/xreef/EByte_LoRa_E220_Series_Library, </br> 
https://github.com/adafruit/DHT-sensor-library, </br> 
https://github.com/GyverLibs/GSON </br>

## UML диаграмма классов ПО оператора

![](https://github.com/CepbluKot/diploma/blob/master/operator_part.png) </br>


## UML диаграмма классов ПО робота

![](https://github.com/CepbluKot/diploma/blob/master/robot_part.png) </br>

## UML диаграмма прецедентов

![](https://github.com/CepbluKot/diploma/blob/master/precedent_diagram.png) </br>

## Графический интерфейс
Вкладка управления и визуализация данных с сенсоров </br>
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/interface.jpeg) </br>

Вкладка выбора типа подключения и отображения состояния подключений </br>
![](https://github.com/CepbluKot/diploma/blob/master/conn_interface.jpeg) </br>

## API для взаимодействия с роботом 
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/api.jpeg) </br>

## Спектрограмма передач при помощи LoRa
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/spectrogram.jpeg) </br>

## Конструкция
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/body.jpg) </br>

## Команда
[Игорь Малыш - программное/аппаратное обеспечение, конструкция](http://t.me/igmalysh) </br>
