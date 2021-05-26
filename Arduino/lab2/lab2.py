# Importing Libraries
import serial
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
cm_value = 0.0

# Initialize communication with TMP102
# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    arduino = serial.Serial(port='/dev/ttyACM2', baudrate=9600, timeout=.1)
    value = arduino.readline()
    
    #arduino.write(b'd')
    arduino.close()

    try:
        #print("CM ",str(value).split(" ")[1]," INCH ",str(value).split(" ")[-2]) # printing the value
        cm_value = float(str(value).split(" ")[1])
        
        
        temp_c = round((cm_value), 2)

        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        ys.append(temp_c)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('TMP102 Temperature over Time')
        plt.ylabel('Temperature (deg C)')
    except:
            #print('error ',value)
        pass

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=50)
plt.show()
