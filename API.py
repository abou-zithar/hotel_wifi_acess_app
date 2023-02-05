from fastapi import FastAPI
from netmiko import ConnectHandler
# from typing import Union

Aruba_Ap = {
    'device_type': 'aruba_os',
    'ip': '192.168.10.182',
    'username': 'admin',
    'password': 'P@$$w0rd',
    'port': '22'
}


app = FastAPI()

AP_Connection = ConnectHandler(**Aruba_Ap)



def get_user_from_Access_point(respond_string):
    users_AP = []
    first_step=respond_string.split('\n')
    second_step=first_step[6:]
    for i in range(len(second_step)):
        users_AP.append(second_step[i].split(' ')[0])
    return users_AP



@app.get("/get_users")
def read_root():
    show_users = AP_Connection.send_command('show users')
    users_AP=get_user_from_Access_point(show_users)
    return {"users": users_AP}




