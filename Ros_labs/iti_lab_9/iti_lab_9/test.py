
import csv


with open('/home/ahmed/ITI_ROS_WS/src/iti_lab_9/iti_lab_9/turtle_commands.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['linear x'],row['angular z'])
