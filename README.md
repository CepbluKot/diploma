[Презентация](https://drive.google.com/file/d/1JERFSXeAEsDtELn5uCYsfifsmstXoqhV/view?usp=sharing) 

## Сборка решения
Проект работает на ОС Linux Ubuntu 22.04 </br>
Для сборки нужен Python 3.8 </br>

```
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.8
sudo apt install python3.8-venv
```

Для корректной работы проекта требуется подключение внешних модулей</br>

Перед сборкой необходимо установить libfreenect: https://github.com/alwynmathew/libfreenect-with-python </br>

Запуск:
```
pip3 install -r requirements.txt
python3 launch_operator_part.py
python3 launch_robot_part.py
```


## Графический интерфейс
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/interface.jpeg) </br>

## Спектрограмма
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/spectrogram.jpeg) </br>

## Конструкция
![](https://github.com/CepbluKot/diploma_gui_ok/blob/master/body.jpg) </br>