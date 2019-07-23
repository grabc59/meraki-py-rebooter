# network-wide reboot tool reboots everything in the specified network

# To Do:
# a way to save the API key to a file. Add that file to git ignore.
# fix network list display so it's more readable
# write my own calls instead of meraki py since those methods print out some unnecessary garbage

# import meraki py for some premade methods, like listing networks in an org
import requests
from prettytable import PrettyTable
from meraki import meraki
import json

# apikey = "fda920e4d397e632a263054ba0e5f405c48ee1f5"

# get API key
apikey = input(f'-> Enter your API key: ')
base_url = 'https://api.meraki.com/api/v0'
# find orgs accessible by this API key
myOrgs = meraki.myorgaccess(apikey)

# print the orgs to select from
orgs_table = PrettyTable()
orgs_table.field_names = ["ID", "Org name"]
for org in myOrgs:
    orgs_table.add_row([org["id"], org["name"]])
print(orgs_table)

# get org ID
print('-> Select the organization that contains the devices you want to reboot')
org_id = input(f'Org ID: ')

# get a list of networks in the organization
# meraki py call:
# def getnetworklist(apikey, orgid, templateid=None, suppressprint=False):
network_list = meraki.getnetworklist(apikey, org_id)
networks_table = PrettyTable()
networks_table.field_names = ["ID", "Network Name"]
for network in network_list:
    networks_table.add_row([network["id"], network["name"]])
print(networks_table)

# get network ID
network_id = input(f'Enter the Network ID containing the devices to reboot: ')

# get a list of devices in the network
# GET/networks/{networkId}/devices
# getnetworkdevices(apikey, networkid, suppressprint=False)
network_devices = meraki.getnetworkdevices(apikey, network_id)

# print out the devices in the network that will be rebooted
devices_table = PrettyTable()
devices_table.field_names = ["Model", "Serial", "MAC", "LAN IP"]
print('Network devices to reboot: ')
for device in network_devices:
    devices_table.add_row(
        [device["model"], device["serial"], device["mac"], device["lanIp"]])
    # print(device)
print(devices_table)

# prompt the user for confirmation to reboot the devices
reboot_confirmation = input(f'Reboot devices now? (y/n) ')

# send reboot call for each device in the network
# reboot API call:
# POST/networks/{networkId}/devices/{serial}/reboot
if reboot_confirmation == 'y':
    results_devices_table = PrettyTable(
        field_names=["Model", "Serial", "MAC", "LAN IP", "Response"])
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)), 'Content-Type': 'application/json'}
    for device in network_devices:
        posturl = '{0}/networks/{1}/devices/{2}/reboot'.format(
            str(base_url), str(network_id), str(device["serial"]))
        r = requests.post(posturl, headers=headers)
        result = r.text
        results_devices_table.add_row(
            [device["model"], device["serial"], device["mac"], device["lanIp"], result])

    print(results_devices_table)
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
