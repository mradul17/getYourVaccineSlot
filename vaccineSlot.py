'''
    File name: vaccineSlot.py
    Author: Mradul Jain
    Date created: 12/05/2021
    Python Version: 3.9.0
'''
import sys
import time
import json
import signal
import requests
from datetime import datetime
import argparse
from win10toast import ToastNotifier
toast = ToastNotifier()

def receiveSignal(signalNumber, frame):
    raise SystemExit('Exit')
    return

def getVaccineSlotDataByPinCode(pincode):
    home_url = "https://www.cowin.gov.in"
    base_url = "https://cdn-api.co-vin.in/api/v2"
    searchByPin= "appointment/sessions/public/calendarByPin"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(home_url, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    date = datetime.now().strftime("%d-%m-%y")
    API = base_url+"/"+searchByPin+"?pincode="+str(pincode)+"&date="+str(date)
    response = session.get(API, headers=headers, timeout=5, cookies=cookies)
    return response.json()
    
def getavailability(data,age_group):
    json_size = len(data['centers'])
    found = 0
    for x in range(0,json_size):
        session_size = len(data['centers'][x]['sessions'])
        for y in range(0,session_size):
            available = data['centers'][x]['sessions'][y]['available_capacity']
            age_limit = data['centers'][x]['sessions'][y]['min_age_limit']
            available_onDate = data['centers'][x]['sessions'][y]['date']
            if available > 0 :
                #print(str(available) + " available on " + available_onDate + " for age group " + str(age_limit))
                if age_group == "all" :
                    found = 1
                    #print(str(available) + " dose available on date " + available_onDate + " for age group " + str(age_limit))
                if age_group == str(age_limit) :
                   found = 1
                   #print(str(available) + " dose available on date " + available_onDate + " for age group " + str(age_limit))
    if found == 1 :       
        toast.show_toast("Notification","Vaccination Dose is available for " + str(age_group) + "+ please visit https://www.cowin.gov.in")
        

def main(pincode,age_group,next_exe_at):
    while(1):
        json_data = getVaccineSlotDataByPinCode(pincode)
        getavailability(json_data,age_group)
        interval = int(next_exe_at)*60
        time.sleep(int(interval))
    
if __name__=="__main__":
    signal.signal(signal.SIGINT, receiveSignal)
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-p','--pin_code',required=True)
    required.add_argument('-t','--time_interval',required=True,help='give this value in minute, After this time interval script will execute again')
    required.add_argument('-a','--age_group',required=True,help='Expected values 18 / 45 / all')
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()   
    if not(args.age_group == "18" or  args.age_group == "45" or  args.age_group == "all") :
        print("wrong age group. choose 18 /45 / all. Please check \'python vaccineSlot.py -h\'")
        sys.exit(1)
    main(args.pin_code,args.age_group,args.time_interval)
    
    
    
    
    
    
    
    
    
    
    