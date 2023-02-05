from netmiko import ConnectHandler
import pandas as pd
import os
import sys

Aruba_Ap = {
    'device_type': 'device_type',
    'ip': 'ip_example',
    'username': 'username',
    'password': 'password',
    'port': 'port_number'
}
GustinfoDataPath=r"D:\mahmoud.gamal\python\HotalWiFiSystem\GustInfo.csv"
TempuserDataPath=r"D:\mahmoud.gamal\python\HotalWiFiSystem\TemporaryAccess.csv"


if os.path.exists(GustinfoDataPath):
    print('The file "Gust info Data Path" Found')
else:
    print('The file does not exist')
    sys.exit()
    



AP_Connection = ConnectHandler(**Aruba_Ap)

def show_user_in_access_point(AP_Connection):
    show_users = AP_Connection.send_command('show users')
    first_step = show_users.split('\n')
    second_step = first_step[6:]
    users_AP = []
    for i in range(len(second_step)):
        users_AP.append(second_step[i].split(' ')[0])
    return users_AP

def add_new_user(AP_Connection,user,password):
    cfg_add = [
        'user <room id> <password> portal',
        'end',
        'commit apply'
    ]
    cfg_add[0] = 'user {} {} portal'.format(user, password)

    AP_Connection.config_mode()
    AP_Connection.send_config_set(cfg_add)

def create_password(last_name):
    password_list=[]
    concat = "{}".format( last_name.lower())
    password_list.append(concat)
    return password_list[0]

def get_user_to_delete(users_AP,Room_ID,Temp_Users):
    user_to_delete = (list(set(users_AP) - set(Room_ID)))
    if os.path.exists(TempuserDataPath):
        user_to_delete = (list(set(user_to_delete) - set(Temp_Users)))
    return user_to_delete

def get_user_to_add(users_AP,Room_ID):
    user_to_add = (list(set(Room_ID) - set(users_AP)))
    return user_to_add

def delete_user_from_access_point(AP_Connection,user):
    cfg_del = [
        'no user <room id>',
        'end',
        'commit apply'
    ]
    cfg_del[0] = 'no user {} '.format(user)
    AP_Connection.config_mode()
    AP_Connection.send_config_set(cfg_del)



if os.path.getsize(GustinfoDataPath) <= 40:
    print("the GustInfo.csv file is empty or not found")
    sys.exit()

#reading data from the sheet and get the features that i want
data = pd.read_csv(GustinfoDataPath)
l_name = data["Last name"]
username = Room_ID = data["RoomID"]
Room_ID.dropna(inplace=True)
Room_ID=[int(x)for x in Room_ID]
Room_ID=[str(x)for x in Room_ID]
password_list_sheet = []






#create a password for the user to add them to the access point
l_name.dropna(inplace=True)

for single_l_name in l_name:
    
    password_list_sheet.append(create_password(single_l_name))


user_to_delete=[]
user_to_add = []
Room_ID=sorted(list(Room_ID))
# get the users from the access point
users_AP=sorted(show_user_in_access_point(AP_Connection))
# if the access point is empty we import the users from the sheet direct
if users_AP == []:
    for i in range(len(Room_ID)):
        add_new_user(AP_Connection, Room_ID[i], password_list_sheet[i])

print("users at Access point",users_AP)

if os.path.exists(TempuserDataPath):
    print('The file "Tempuser Data Path" Found')
    if os.path.getsize(TempuserDataPath) <= 40:
        print("the TemporaryAccess.csv file is empty or not found")
        sys.exit()
    tempUsersData=pd.read_csv(TempuserDataPath)
    Temp_Users=tempUsersData['UserName']
    # print(Temp_Users)
    user_to_delete=get_user_to_delete(users_AP,Room_ID,Temp_Users)
else:
    user_to_delete=get_user_to_delete(users_AP,Room_ID,[])


# get the users that we ant to delete and the user to add
user_to_add=get_user_to_add(users_AP,Room_ID)

print("users to add",user_to_add)
print("users to delete",user_to_delete)

if user_to_delete:
    for user in user_to_delete:
        delete_user_from_access_point(AP_Connection, user)

if user_to_add:
    last_name_of_people_to_add = []
    for user in user_to_add:
        last_name_of_people_to_add.append(data.loc[data['RoomID'] == int(user)]['Last name'].values[0])
    password_list_of_users_to_add = []
    for i in range(len(user_to_add)):
        password_list_of_users_to_add.append(create_password( last_name_of_people_to_add[i]))
    for i in range(len(user_to_add)):
        add_new_user(AP_Connection,user_to_add[i],password_list_of_users_to_add[i])

users_AP=show_user_in_access_point(AP_Connection)
AP_Connection.save_config()
print("Current users",users_AP)

print("------------------")
print(f"the passwords:{password_list_sheet}")
print("-------------------")

print("Closing Connection")
AP_Connection.disconnect()

