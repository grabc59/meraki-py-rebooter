# network-wide reboot tool

# To Do:
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
    for device in network_devices:
        r = requests.post('https://httpbin.org/post', data={'key': 'value'})
