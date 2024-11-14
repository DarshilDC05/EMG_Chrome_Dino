import serial
import pyautogui
# Set up serial communication with Arduino
arduino_port = 'COM3'  # Change this to your Arduino port
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate)

l = []
n = 1
threshold = 150     

# Main loop to read data from Arduino and plot
try:
    while True:
        # Read data from Arduino
        try:
            signal, envelope = ser.readline().decode('utf-8').strip().split(',')
        except:
            continue

        # Check if data is valid
        if not signal:
            continue

        emg_value = float(envelope)

        l.append(emg_value >= threshold)
        if len(l) > 2 * n:
            l.pop(0)
        # print(signal, envelope, emg_value >= threshold, l)
        
        if len(l) == 2 * n:
            x = sum(l[:n])
            y = sum(l[n:])
            if y - x >= n:
                print("Jump")
                pyautogui.press('space')

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()