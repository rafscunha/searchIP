from ReaderTerminal import ReaderTerminal
from SearchIP import SearchIP

terminal = ReaderTerminal(element='externo')
info = SearchIP()

ip_list = terminal.get()
for ip in ip_list[terminal.campos[2]]:
    if info.validateIP(ip):
        info_ip = info.get(ip)
        print("IP: {} -> {}".format(ip, info_ip))

