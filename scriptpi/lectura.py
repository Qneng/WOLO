import MySQLdb
import RPi.GPIO as GPIO
import waker as Waker

from pn532 import *


if __name__ == '__main__':
    try:

        pn532 = PN532_UART(debug=False)

        
        pn532.SAM_configuration()
        check = True
       
        while check == True:
            # Este comando lee la tarjeta.
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            decodi=uid.decode('utf-8')
            decodi=decodi.replace("[", "")
            decodi=decodi.replace("]", "")
            # Vuelve a intentarlo si no encuentra tarjeta.


# En este comando se debe cambiar la información en este orden "IP, Usuario, Contraseña, Nombre de la base de"
            db=MySQLdb.connect("192.168.0.33","alex","alex","wake")

            curmac = db.cursor()

            curmac.execute("select MAC from nfc where cardid= %s", (decodi,))

            mac = curmac.fetchall()


            for item in mac:
                mac = item[0]

            curip = db.cursor()

            curip.execute("select ip from nfc where cardid= %s", (decodi,))

            ip = curip.fetchall()
            for item in ip:
                ip = item[0]


            db.close()
#             mac = "30:9C:23:81:DA:CB"
#             ip = "192.168.0.29"
            port = 7
            wol = Waker.Waker()
            wol.makeMagicPacket(mac)
            wol.sendPacket(wol.packet, ip, port)
            print ('Packet successfully sent to')
            
            # Vuelve a intentarlo si no encuentra tarjeta.
            if uid is None:
                continue
            print('Se ha encontrado la tarjeta :', [hex(i) for i in uid])
            check = False
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()