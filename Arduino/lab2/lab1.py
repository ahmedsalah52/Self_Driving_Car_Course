def save(line,speed):
    f = open('python_test_file_2.txt','a')
    f.write(line)
    f.write('\n')
    f.write(',speed ')
    f.write(str(speed))
    f.write('\n')
    f.close() 



with open('python_test_file.txt') as f:
    lines = f.read().split('\n')

for line in lines:
    speed = 0
    for value in line.split(',')[-3:]:
        try:
            speed += (float(value)**2)
        except:
            pass
    if speed != 0:
        save(line,speed)

	