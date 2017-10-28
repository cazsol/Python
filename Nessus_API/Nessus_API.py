"""
THIS SECTION IMPORTS CERTAIN LIBRARIES NEEDED AND ESTABLISHES SOME PARAMETERS
"""
import requests
import json
import time
import sys
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url = 'https://10.1.5.250:8834' # IP of the server running Nessus
verify = False
token = ''
username = "SecurityChathamAdmin"
password = "Seris^6sieS1"
mode = input('Please select a mode to run [1]: update scans, [2]: download results ')
#username = input('Please input username: ')
#password = getpass.getpass('Please input password: ')
"""
END OF SECTION
"""
"""
THIS SECTIONS CONTAINS CODE USED TO REFRESH THE LIST OF TARGETS OF THE SCANS
"""
### THIS IS A HARDCODED DICTIONARY of vlan name [1] and Nessus scans name [2]
### IF YOU WANT TO ADD ANOTHER SCAN OR CHANGE THE SCAN IN WHICH A VLAN SHOULD BE
### CONTAINED,PLEASE UPDATE THIS DICTIONARY
Z = {'Undefined':'Vlan_Undefined',
'VLAN 1':'Vlan_1',
'vlan 10 JKM':'Vlans_JKM',
'vlan 11 JKM IT':'Vlans_JKM',
'vlan 12 JKM 3rd floor':'Vlans_JKM',
'vlan 13 JKM Lab':'Vlans_JKM',
'vlan 14 JKM Lab':'Vlans_JKM',
'VLAN 15 Switches':'Vlan_15_Switches',
'vlan 16 Compellent Management':'Small_Vlans',
'vlan 19 Eddy':'Small_Vlans',
'vlan 20 BFC':'Vlan_20_BFC',
'vlan 21 Buhl Basement':'Vlan_21_Buhl_Basement',
'vlan 22 Buhl Ground Floor':'Vlan_22_Buhl_Ground_Floor',
'vlan 23 Braun Falk':'Vlan_23_Braun_Falk',
'vlan 24 Woodland Staff':'Vlan_24_Woodland_Staff',
'vlan 25 Laughlin Music':'Small_Vlans',
'vlan 250 Wireless':'Vlan_250_Wireless',
'vlan 26 Fickes':'Small_Vlans',
'vlan 27 Beatty 1st Floor':'Vlan_27_and_29',
'vlan 28 Berry':'Vlan_28_Berry',
'vlan 29 Beatty 2nd Floor':'Vlan_27_and_29',
'vlan 30 Rea Garage':'Small_Vlans',
'vlan 32 Laughlin Hall':'Small_Vlans',
'vlan 33 ADC':'Vlan_33_ADC',
'vlan 34 AFC':'Small_Vlans',
'vlan 35 Carriage House':'Small_Vlans',
'vlan 36 Dilworth':'Small_Vlans',
'vlan 37 Mellon Basement':'Vlan_37_and_38',
'vlan 38 Mellon 3rd Floor':'Vlan_37_and_38',
'vlan 39 Chapel':'Small_Vlans',
'vlan 40 Woodland Res':'Small_Vlans',
'vlan 41 Lindsay House':'Small_Vlans',
'vlan 43 Gatehouse':'Small_Vlans',
'vlan 80 Eden Servers/Computers':'Vlan_80_and_81',
'vlan 81 Eden HVAC':'Vlan_80_and_81',
'vlan 87 Eastside Servers/Computers':'Vlan_87_Eastside',
'vlan 88 Eastside Servers/Computers':'Vlan_88_Eastside',
'vlan 89 Eastside Servers/Computers':'Vlan_89_Eastside',
'vlan 90 Eastside Phones/Printers':'Vlan_90_Eastside',
'vlan 92 Imaging':'Vlan_92_Imaging'}
# READS THE FILE WITH ALL THE INFORMATION OF HOSTS IN THE NETWORK
def inputIPs():
    listaIps = open('web50getassetgroups.csv', 'r')
    return listaIps
# DEFINES THE ORDER OF THE SORTING FOR THE LIST
def getKey(item):
    return item[1]
# CREATES A STRING OF IPs THAT IS PASSED TO THE UPDATE FUNCTION, WITH THE SCAN
# NAME TO UPDATE THE SCAN WITH THE REFRESHED IPs
def createTargets(listToSeparate, scansList):
    for x in scansList:
        z = ""
        for y in listToSeparate:
            if y[1] == x:
                z += y[0]+", "
            else:
                continue
        scanID = ""
        i = 0
        for r in scanNameAndID:
            if  x == scanNameAndID[i][0]:
                scanID = scanNameAndID[i][1]
                i += 1
            else:
                i += 1
                continue
        update(scanID,x,"Updated", z)
        print("Scan "+x+" has been updated")
# CONTROLS THE FLOW OF THE UPDATE SECTION OF THE CODE
def cretateTargetsLists():
    output = []
    scans = []
    lista = inputIPs()
    header = lista.readline()
    header = header.split(';')
    vlanPosition = header.index('"IPLocation"')
    IPPosition = header.index('"IP Address"')
    for line in lista:
        try:
            client = line
            client = client.split('";"')
            if client[IPPosition] == '':
                continue
            ip = [client[IPPosition],Z[client[vlanPosition]]]
            scanner = ip[1]
            output.append(ip) # output takes the info of IP and Vlan
            scans.append(scanner) # this only has the information of Vlan
        except IndexError:
            continue
    output = sorted(output, key=getKey)
    scansList = set(scans)
    scansList = list(scansList)
    createTargets(output,scansList)
"""
END OF SECTION
"""
"""
THIS SECTION CONTROLS THE INTERACTION WITH THE API
"""
# THIS FUNCTION CREATES THE URL USING THE URL PROVIDED AND THE TYPE OF REQUESTS BEING MADE "SESSION" FOR EXAMPLE
def build_url(resource):
    return '{0}{1}'.format(url, resource) # {0}{1} INDICATES THE ORDER OF THE ARGUMENTS PASSED
# THIS FUNCTION MAKES THE CONNECTION TO THE CLIENT METHOD: GET, POST; RESOURCE IS USED TO INDICATE WHAT IT IS REQUESTED; DATA PASSES THE ARGUMENTS NEEDED
def connect(method, resource, data=None):
    # CREATES THE HEADERS NEEDED TO PASS IN THE REQUESTS
    headers = {'X-Cookie': 'token={0}'.format(token),
               'content-type': 'application/json'}
    # TOKEN IS NOT USED IN THE FIRST CONNECTION, AFTER LOG IN IT IS USED
    data = json.dumps(data) # JSON.DUMPS() ENCODES DATA IN JAVASCRIPT OBJECT NOTATION, SO IT CAN BE USED IN THE REQUEST
    # MAKES THE REQUESTS ACCORDING TO THE INFORMATION REQUIRED
    if method == 'POST':
        r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
    else:
        r = requests.get(build_url(resource), params=data, headers=headers, verify=verify)
    # Exit if there is an error.
    if r.status_code != 200:
        e = r.json()
        print(e)
        sys.exit()
    # When downloading a scan it passes contents not the JSON data.
    if 'download' in resource:
        return r.content
    else:
        return r.json()
# THIS RETURNS THE TOKEN USED IN THE OTHER REQUESTS
def login(usr, pwd):
    login = {'username': usr, 'password': pwd} # PASSES USER AND PASSWORD
    data = connect('POST', '/session', data=login)
    return data['token'] # RETURNS THE TOKEN
# THIS FUNCTION GETS INFORMATION OF THE ALL SCANS
def get_name():
    data = connect('GET', '/scans')
    lista = []
    # APPENDS INFO TO ONE LIST
    for p in data['scans']:
        x = [p['name'], p['uuid'], p['id'], p['status']]
        lista.append(x)
    return lista # RETURNS THE LIST WITH THE INFO
# THIS FUNCTION RETURNS THE HISTORY ID OF THE SCANS
def get_history(scan_id, name):
    data = connect('GET', '/scans/{0}'.format(scan_id))
    lista = []
    # STARTS A LOOP TO RECOVER INFO FROM SCANS BY ID, ONLY COMPLETED SCANS
    if data['history'] != None:
        for p in data['history']:
            x = [scan_id, p['uuid'], p['history_id'], p['status'], name]
            print(x)
            if x[3] == 'completed':
                lista.append(x)
    return lista # RETUNRS INFO IN A LIST
# RETURNS THE ITEM WITH THE HIGHEST VALUE IN AN INDEX
def highest_id(lista_ids):
    orden = sorted(lista_ids, key=lambda x: x[2]) # orders the list according the third element
    items = len(orden)-1 # gets the index for the last element in the list
    return lista_ids[items] # returns a list with the highest value in the third position
# UPDATES MUTIPLE PARAMETERS OF THE SCANS
def update(scan_id, name, desc, targets, pid=None):
    scan = {}
    scan['settings'] = {}
    scan['settings']['name'] = name
    scan['settings']['description'] = desc
    scan['settings']['text_targets'] = targets
    if pid is not None:
        scan['uuid'] = pid
    data = connect('PUT', '/scans/{0}'.format(scan_id), data=scan)
# VERIFIES THE EXPORT STATUS OF A SCAN: IF IT IS READY
def export_status(sid, fid):
    print("export status has started")
    data = connect('GET', '/scans/{0}/export/{1}/status'.format(sid, fid))
    return data['status'] == 'ready'
# GENERATES THE FILE ID, THAT IS USED TO DOWNLOAD THE RESULTS OF THE SCAN
def export(sid, hid):
    data = {'history_id': hid,
            'format': 'csv'}
    data = connect('POST', '/scans/{0}/export'.format(sid), data=data)
    fid = data['file']
    while export_status(sid, fid) is False:
        time.sleep(5)
    return fid
# DOWNLOADS THE SCAN RESULTS
def download(sid, fid, name):
    name = name.replace("/", "_")
    data = connect('GET', '/scans/{0}/export/{1}/download'.format(sid, fid))
    filename = '{0}.csv'.format(name)
    data = str(data).strip("b'")
    lines = data.split("\\n")
    f = open(filename, "w")
    for line in lines:
       line = line.strip("\\r")
       f.write(line + "\n")
    f.close()
if __name__ == '__main__':
    if mode == 1:
        print("Scans will be updated")
        token = login(username, password)
        listaNombres = get_name()
        scanNameAndID = []
        i = 0
        for x in listaNombres:
            if listaNombres[i][3] != "imported":
                element = [listaNombres[i][0], listaNombres[i][2]]
                scanNameAndID.append(element)
                i += 1
            else:
                i += 1
                continue
        cretateTargetsLists()
        print("Scans have been updated")
    elif mode == 2:
        token = login(username, password)
        listaNombres = get_name()
        i = 0
        listaHistoria = []
        listaFinales = []
        for x in listaNombres:
        #    if listaNombres[i][3] == 'completed':
            lista_hids = get_history(listaNombres[i][2], listaNombres[i][0])
            if not lista_hids:
                i += 1
                continue
            else:
                altisimo_hid = highest_id(lista_hids)
            listaFinales.append(altisimo_hid)
            i += 1
        i = 0
        for x in listaFinales:
            scan_id = listaFinales[i][0]
            history_id = listaFinales[i][2]
            name = listaFinales[i][4]
            file_id = export(scan_id, history_id)
            print(str(scan_id)+", "+str(file_id)+", "+str(name))
            download(scan_id, file_id, name)
            print(name+" was donwloaded")
            i += 1
    print('Logout')
