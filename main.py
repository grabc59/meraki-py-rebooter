# network-wide reboot tool

# To Do:
# Next, write reboot post call

# add a way to save the api key rather than entering it every time the application is run
# fix network list display so it's more readable
# write my own calls instead of meraki py since those methods print

# import meraki py for some premade methods, like listing networks in an org
from meraki import meraki
import requests

# apikey = "fda920e4d397e632a263054ba0e5f405c48ee1f5"
# print(myOrgs)

# get API key
apikey = input(f'-> Enter your API key: ')

base_url = 'https://api.meraki.com/api/v0'

# find orgs accessible by this API key
myOrgs = meraki.myorgaccess(apikey)

# print the orgs to select from
print('Organization ID, Name')
for org in myOrgs:
    print(org)
    # print(f'ID: {org.id}, Name: {org.name}')

# get org ID
print('-> Select the organization that contains the devices you want to reboot')
org_id = input(f'Org ID: ')

# get a list of networks in the organization
# meraki py call:
# def getnetworklist(apikey, orgid, templateid=None, suppressprint=False):
network_list = meraki.getnetworklist(apikey, org_id)

for network in network_list:
    print(network)

# get network ID
network_id = input(f'Enter the Network ID containing the devices to reboot: ')

# get a list of devices in the network
# GET/networks/{networkId}/devices
# getnetworkdevices(apikey, networkid, suppressprint=False)
network_devices = meraki.getnetworkdevices(apikey, network_id)

# print out the devices in the network that will be rebooted
print('Network devices to reboot: ')
for device in network_devices:
    print(device)

# prompt the user for confirmation to reboot the devices
reboot_confirmation = input(f'Reboot devices now? (y/n) ')

# send reboot call for each device in the network
# reboot API call:
# POST/networks/{networkId}/devices/{serial}/reboot
if reboot_confirmation == 'y':
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)), 'Content-Type': 'application/json'}
    for device in network_devices:
        posturl = '{0}/networks/{1}/devices/{2}/reboot'.format(
            str(base_url), str(network_id), str(device["serial"]))
        r = requests.post(posturl, headers=headers)
        # dashboard = requests.post(posturl, headers=headers)
        print(r)
        print(r.text)

# Remove a single device
# https://api.meraki.com/api_docs#remove-a-single-device
# def removedevfromnet(apikey, networkid, serial, suppressprint=False):
#     calltype = 'Device'
#     posturl = '{0}/networks/{1}/devices/{2}/remove'.format(
#         str(base_url), str(networkid), str(serial))
#     headers = {
#         'x-cisco-meraki-api-key': format(str(apikey)),
#         'Content-Type': 'application/json'
#     }
#     dashboard = requests.post(posturl, headers=headers)
#     #
#     # Call return handler function to parse Dashboard response
#     #
#     result = __returnhandler(
#         dashboard.status_code, dashboard.text, calltype, suppressprint)
#     return result
