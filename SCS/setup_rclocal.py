import os

with open('/etc/rc.local', 'r') as file:
    data = file.read()


k = data.rfind('exit 0')



dir_path = os.path.dirname(os.path.realpath(__file__))

new_string = data[:k] + "\ncd " + dir_path + "/APP/" + "\nsudo python3 " + dir_path + "/APP/main.py\nexit 0"


with open('/etc/rc.local', 'w') as file:
    file.write(new_string)

#print(os.popen("sudo node-red-stop").read())
