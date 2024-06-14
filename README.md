## ВКР на тему "Разработка мобильного робота для выполнения логистических операций"


[Презентация](https://drive.google.com/file/d/1JERFSXeAEsDtELn5uCYsfifsmstXoqhV/view?usp=sharing) </br>
[Отчет](https://drive.google.com/file/d/10wPHXu9SVHKw2DTHqq66AvC2ev5tR8jF/view?usp=sharing) </br>


## Состав решения
mcu_modules - ПО, запускаемое на аппаратном обеспечении на микроконтролерах ATmega328P</br>
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

Для корректной работы проекта требуется подключение модулей аппаратного обеспечения</br>
Материалы по сборке элементов аппаратного обеспечения представлены в приложении отчета, доступного по указанной выше ссылке</br>

Перед сборкой необходимо установить libfreenect (собирать под python 3.8): https://github.com/alwynmathew/libfreenect-with-python </br>

Запуск:
```
pip3 install -r requirements.txt
python3 launch_operator_part.py
python3 launch_robot_part.py
```

Сборка ПО для микроконтроллеров выполнялась при помощи https://platformio.org/ </br>
Для сборки ПО для микроконтроллеров применяются библиотеки: https://github.com/xreef/EByte_LoRa_E220_Series_Library, https://github.com/adafruit/DHT-sensor-library, https://github.com/GyverLibs/GSON </br>

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
