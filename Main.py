import RPi.GPIO as GPIO
import keyboard
import serial

key_list = [
            ["`",40,False],["1",41,False],["2",42,False],["3",43,False],["4",44,False],["5",45,False],["6",46,False],["7",47,False],["8",48,False],["9",49,False],["0",50,False],["-",51,False],["=",52,False],["backspace",53,False],
            ["q",54,False],["w",55,False],["e",56,False],["r",57,False],["t",58,False],["y",59,False],["u",60,False],["i",61,False],["o",62,False],["p",63,False],["[",64,False],["]",65,False],["#",66,False],
            ["a",67,False],["s",68,False],["d",69,False],["f",70,False],["g",71,False],["h",72,False],["j",73,False],["k",74,False],["l",75,False],[";",76,False],["'",77,False],["enter",78,False],
            ["z",79,False],["x",80,False],["c",81,False],["v",82,False],["b",83,False],["n",84,False],["m",85,False],[",",86,False],[".",87,False],["/",88,False]

        ]

key_push_list = []

SerDevice = serial.Serial('/dev/ttyAMA0',baudrate=31250)

CH = 0
octave = 0
NOTE_ON = 9
NOTE_OFF = 8

def send_midi(switch,note,vel):
    SerDevice.write(bytearray([(switch << 4) | CH,note + 12 * octave,vel]))



def key_send_midi():
    for key_state in key_list:
        if keyboard.is_pressed(key_state[0]):
            if not key_state[2]:
                send_midi(NOTE_ON,key_state[1],127)
                key_state[2] = True
                print(key_state[0] + " : ON")
        else:
            if key_state[2]:
                send_midi(NOTE_OFF,key_state[1],0)
                key_state[2] = False
                print(key_state[0] + " : OFF")


try:
    while True:
        key_send_midi()
        if keyboard.is_pressed("up"):
            octave = octave + 1
            if octave > 2:
                octave = 2
        elif keyboard.is_pressed("down"):
            octave = octave - 1
            if octave < -2 :
                octave = -2

except KeyboardInterrupt:
    GPIO.cleanup()

