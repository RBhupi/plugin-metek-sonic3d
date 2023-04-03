import numpy as np
import serial
from waggle.plugin import Plugin
from argparse import ArgumentParser


def main(args):
    ser = serial.Serial(args.device, baudrate=args.baud_rate,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)
    ser.flushInput()
    
    #print("Wind direction, wind speed, units")



    with Plugin() as plugin:
        while True:
            try:
                text = str(ser.readline(), 'utf-8').strip()
            except Exception as e:
                plugin.publish('exit.status' , e)
                break
            
            text_split = text.split(';')
            wx =  text_split[1]
            wy = text_split[2]
            wz = text_split[3]
            temperature = text_split[4]
            plugin.publish("sonic3d.Wx.mps", wx)
            plugin.publish("sonic3d.Wy.mps", wy)
            plugin.publish("sonic3d.Wz.mps", wz)
            plugin.publish("sonic3d.T.celcius", temperature)


    if not ser.closed:
        ser.close()


if __name__ == "__main__":
    parser = ArgumentParser(
        description="plugin for pushing windsonic 2d anemometer data through WSN")

    parser.add_argument('--device', type=str, dest='device',
                        default='/dev/ttyUSB0', help='device to read')
    parser.add_argument('--baud_rate', type=int, dest='baud_rate',
                        default=9600, help='baud rate for the device')

    args = parser.parse_args()

    main(args)