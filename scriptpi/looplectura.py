from time import sleep


while True:
    try:
        sleep(0.5)
        exec(open("lectura.py").read())
    except Exception as e:
         exec(open("lectura.py").read())