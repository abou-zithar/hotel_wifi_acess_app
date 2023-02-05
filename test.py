
from netmiko import ConnectHandler
# from typing import Union


Aruba_Ap = {
    'device_type': 'aruba_os',
    'ip': '192.168.10.182',
    'username': 'admin',
    'password': 'P@$$w0rd',
    'port': '22'
}

AP_Connection = ConnectHandler(**Aruba_Ap)

show_users = AP_Connection.send_command('show users')
print(show_users)