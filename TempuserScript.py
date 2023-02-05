from netmiko import ConnectHandler
import pandas as pd
from datetime import datetime
import numpy as np
import os
import sys

GustinfoDataPath=r"D:\mahmoud.gamal\python\HotalWiFiSystem\GustInfo.csv"
TempuserDataPath=r"D:\mahmoud.gamal\python\HotalWiFiSystem\TemporaryAccess.csv"

if os.path.exists(TempuserDataPath):
    print('The file "Tempuser Data Path" Found')
else:
    print('The file does not exist')
    sys.exit()

Aruba_Ap = {
    'device_type': 'device_type',
    'ip': 'ip_example',
    'username': 'username',
    'password': 'password',
    'port': 'port_number'
}

AP_Connection = ConnectHandler(**Aruba_Ap)

def delete_user_from_access_point(AP_Connection,user):
    cfg_del = [
        'no user <room id>',
        'end',
        'commit apply'
    ]
    cfg_del[0] = 'no user {} '.format(user)
    AP_Connection.config_mode()
    AP_Connection.send_config_set(cfg_del)

def add_new_user(AP_Connection,user,password):
    cfg_add = [
        'user <room id> <password> portal',
        'end',
        'commit apply'
    ]
    cfg_add[0] = 'user {} {} portal'.format(user, password)
    AP_Connection.config_mode()
    AP_Connection.send_config_set(cfg_add)

def show_user_in_access_point(AP_Connection):
    show_users = AP_Connection.send_command('show users')
    first_step = show_users.split('\n')
    second_step = first_step[6:]
    users_AP = []
    for i in range(len(second_step)):
        users_AP.append(second_step[i].split(' ')[0])
    return users_AP

if os.path.getsize(TempuserDataPath) <= 40:
    print("the TemporaryAccess.csv file is empty or not found")
    sys.exit()



print("before : ",show_user_in_access_point(AP_Connection=AP_Connection))

tempUsersData=pd.read_csv(TempuserDataPath)

accessDates=tempUsersData["AccessDate"]
Users=tempUsersData['UserName']
accessDates_list_from=[]
accessDates_list_to=[]
from_datetime_list=[]
to_datetime_list=[]


for accessDate in accessDates:
    list_date=accessDate.split("-")
    accessDates_list_from.append(list_date[0])
    accessDates_list_to.append(list_date[1])

def get_user_to_delete(users_AP,Temp_Users,normal_users):
    user_to_delete = (list(set(users_AP) - set(Temp_Users)))
    if os.path.exists(GustinfoDataPath):
        # print(normal_users)
        user_to_delete = (list(set(user_to_delete) - set(normal_users)))
    return user_to_delete

def check_date(AP_Connection,user,password,to_date):
    current_date = datetime.now()
    current_date= np.datetime64(current_date)
    if to_date< current_date:
        #delete from the access point
        delete_user_from_access_point(AP_Connection, user)
      
    else:
        # the user is still using the temp
        add_new_user(AP_Connection, user, password)

def Convert_access_To_date_to_time(accessDate):
    formatter_string = ' %m/%d/%Y %H:%M %p'
    datetime_object = datetime.strptime(accessDate, formatter_string)
    return datetime_object

def Convert_access_From_date_to_time(accessDate):
    formatter_string = '%m/%d/%Y %H:%M %p '
    datetime_object = datetime.strptime(accessDate, formatter_string)
    return datetime_object


for date in accessDates_list_from:
    from_datetime_list.append(Convert_access_From_date_to_time(date))

for date in accessDates_list_to:
    to_datetime_list.append(Convert_access_To_date_to_time(date))

tempUsersData['AccessDate_From']=from_datetime_list
tempUsersData['AccessDate_to']=to_datetime_list
tempUsersData.drop(['AccessDate'],axis=1,inplace=True)


# the logic if the to date is smaller than the current then delete from the access point 
# if not don't do ant thing and save the users ids to read them in the main script 
###############################################################################################################


Access_point_user=show_user_in_access_point(AP_Connection)

for i,user in enumerate(Users) :
    check_date(
    AP_Connection,
    user,
    tempUsersData.loc[tempUsersData['UserName']==user]['Password'].values[0],
    tempUsersData.loc[tempUsersData['UserName']==user]['AccessDate_to'].values[0])


if os.path.exists(GustinfoDataPath):
    print('The file "Gust info Data Path" Found')
    if os.path.getsize(GustinfoDataPath) <= 20:
        print("the GustInfo.csv file is empty or not found")
        sys.exit()
    data = pd.read_csv(GustinfoDataPath)
    username = Room_ID = data["RoomID"]
    Room_ID=[int(x)for x in Room_ID]
    Room_ID=[str(x)for x in Room_ID]
    user_to_delete=get_user_to_delete(Access_point_user,Users,Room_ID)

else:

    user_to_delete=get_user_to_delete(Access_point_user,Users,[])




if user_to_delete:
    for temp_user in user_to_delete:
        delete_user_from_access_point(AP_Connection, temp_user)

print("after : ",show_user_in_access_point(AP_Connection=AP_Connection))