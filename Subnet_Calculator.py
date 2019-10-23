import os
import sys
import linecache
import ipaddress
import platform
import subprocess


def get_ip_and_mask():
    os.system("ipconfig | find {} > subnet_info.txt".format('"IPv4 Address. . . . . . . . . . . : "'))
    os.system("ipconfig | find {} >> subnet_info.txt".format('"Subnet Mask . . . . . . . . . . . : "'))
    ip = linecache.getline("subnet_info.txt", 1).split(": ")[1].replace('\n', '')
    mask = linecache.getline("subnet_info.txt", 2).split(": ")[1].replace('\n', '')
    return ip + "/" + mask


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    return subprocess.call(command)


def is_addr_val(address):
    valid = True
    try:
        address = address.split('/')
        ip = address[0].split('.')
        mask = address[1].split('.')
    except IndexError:
        print("Incorrectly entered address !")
        return False
    if len(ip) == 4 and len(mask) == 4:
        for ip_part, mask_part in zip(ip, mask):
            try:
                ip_part, mask_part = int(ip_part), int(mask_part)
            except (ValueError, TypeError):
                print("IP and mask must be numbers !")
                valid = False
                break
            if 0 <= ip_part <= 255 and 0 <= mask_part <= 255:
                pass
            else:
                print("Octet is not in range <0, 255> !")
                valid = False
                break
    else:
        print("IP has not 4 octets !")
        valid = False
    return valid


def network_class(ip):
    first = ip[:ip.find('.')]
    if int(first) < 128:
        return "A"
    elif int(first) < 192:
        return "B"
    elif int(first) < 224:
        return "C"
    elif int(first) < 240:
        return "D"
    else:
        return "E"


def dec_to_bin(dec):
    dec = dec.split('.')
    bin_version = []
    for dec_part in dec:
        bin_version.append(str(format(int(dec_part), '#010b'))[2:])
    bin_version = '.'.join(bin_version)
    return bin_version


def logic_and(address):
    address1 = dec_to_bin(address.split('/')[0])
    address2 = address.split('/')[1]
    address3 = dec_to_bin(address2)
    result = ""
    for i in range(len(address1)):
        if address1[i] == '.':
            result += '.'
        else:
            result += str(int(address1[i]) * int(address3[i]))
    result = result.split('.')
    for i in range(len(result)):
        result[i] = str(int(result[i], 2))
    result = '.'.join(result) + "/" + address2
    return result


def calculate(address):
    file = open('Results.txt', 'a')

    print("Address: ", address)
    file.write("Address: " + address + "\n")
    print("IP: ", address.split('/')[0])
    file.write("IP: " + address.split('/')[0] + "\n")
    print("Mask in dec: ", address.split('/')[1], " In bin: ", dec_to_bin(address.split('/')[1]))
    file.write("Mask in dec: " + address.split('/')[1] + " In bin: " + dec_to_bin(address.split('/')[1]) + "\n")
    network = ipaddress.IPv4Network(logic_and(address))
    print("Network address: ", network.network_address)
    file.write("Network address: " + str(network.network_address) + "\n")
    print("Network class: ", network_class(str(network)))
    file.write("Network class: " + network_class(str(network)) + "\n")
    if network.is_private:
        print("Address type: private")
        file.write("Address type: private\n")
    else:
        print("Address type: public")
        file.write("Address type: public\n")
    print("Broadcast in dec: ", network.broadcast_address, " In bin: ", dec_to_bin(str(network.broadcast_address)))
    file.write("Broadcast in dec: " + str(network.broadcast_address) + " In bin: " +
               dec_to_bin(str(network.broadcast_address)) + "\n")
    hosts = list(ipaddress.ip_network(logic_and(address)).hosts())
    print("First host address in dec: ", hosts[0], " In bin: ", dec_to_bin(str(hosts[0])))
    file.write("First host address in dec: " + str(hosts[0]) + " In bin: " + dec_to_bin(str(hosts[0])) + "\n")
    print("Last host address in dec: ", str(hosts[-1]), " In bin: ", dec_to_bin(str(hosts[-1])))
    file.write("Last host address in dec: " + str(hosts[-1]) + " In bin: " + dec_to_bin(str(hosts[-1])) + "\n")
    print("The maximum number of hosts that can be assigned to the subnet: ", str(len(hosts)))
    file.write("The maximum number of hosts that can be assigned to the subnet: " + str(len(hosts)) + "\n\n\n")

    file.close()

    if address.split('/')[0] == get_ip_and_mask().split('/')[0]:
        print("The given address is the host's address. Do you want to ping? (Enter 'Y' if you want to)")
        if input() == "Y":
            ping(address.split('/')[0])


def cidr_to_ip(cidr):
    cidr = int(cidr)
    result = ""
    for i in range(1, 33):
        if i > 1 and (i - 1) % 8 == 0:
            result += "."
        if cidr > 0:
            result += '1'
            cidr -= 1
        else:
            result += '0'
            cidr -= 1
    result = result.split('.')
    for i in range(len(result)):
        result[i] = str(int(result[i], 2))
    result = '.'.join(result)
    return result


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def main():
    while True:
        choice_1 = int(input("What do you want to do?\n1 - Calculate the subnet\n2 - Exit\nYour choice: "))
        while True:
            if choice_1 == 1:
                break
            elif choice_1 == 2:
                sys.exit(0)
            else:
                choice_1 = int(input("Incorrect command !\nTry again: "))

        if len(sys.argv) > 1:
            choice_2 = 1
        else:
            choice_2 = 2
        while True:
            if choice_2 == 1:
                # address = input("Enter the address in the format 'ip/mask': ")
                address = sys.argv[1]
                alist = address.split('/')
                if len(alist) != 2:
                    print("No mask entered !")
                    break
                if len(address.split('/')[1]) <= 2:
                    address = address.split('/')
                    address[1] = cidr_to_ip(address[1])
                    address = '/'.join(address)
                break
            elif choice_2 == 2:
                address = get_ip_and_mask()
                break
            else:
                choice_2 = int(input("Incorrect command !\nTry again: "))

        if is_addr_val(address):
            calculate(address)

        input("Press any key to continue...")
        clear()


main()
