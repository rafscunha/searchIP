from ReaderTerminal import ReaderTerminal
from SearchIP import SearchIP
import os
import time

"""
ip_list = terminal.get()
for ip in ip_list[terminal.campos[2]]:
    if info.validateIP(ip):
        info_ip = info.get(ip)
        print("IP: {} -> {}".format(ip, info_ip))
"""


class Programa:
    def  __init__(self):
        self.terminal = ReaderTerminal(element='externo')
        self.info = SearchIP()
        pass
    #-----------------------------------------------------------------------------------------------

    def printData(self, ip, dicionario):
        
        string = "IP: {:15}".format(ip)
        for dado in dicionario:
            try:
                string += " - {} : {}".format(dado, dicionario[dado])
            except:
                pass
        pass
        return string
    #-----------------------------------------------------------------------------------------------
    def consultaDatabase(self):
        #os.system('cls')
        ips = self.info.getDatabase()
        #print(ips)
        
        for ip in ips:
            dados = ips[ip]
            string = self.printData(ip, dados)
            print(string)
                    
        bla = input("\n Pressione Enter para continuar...")
        return
    #-----------------------------------------------------------------------------------------------
    def seeAllConnections(self):
        ip_list = self.terminal.get()
        for ip in ip_list[self.terminal.campos[2]]:
            if self.info.validateIP(ip):
                info_ip = self.info.get(ip)
                string = self.printData(ip, info_ip)
                print(string)
        bla = input("\n Pressione Enter para continuar...")
        pass

    #-----------------------------------------------------------------------------------------------
    def continueRead(self):
        """
        list_now = {}
        list_init = self.terminal.get()
        ips = list_init[self.terminal.campos[2]]
        estados = list_init[self.terminal.campos[3]]
        for index in range(len(ips)):
            if self.info.validateIP(ips[index]) :
                info_ip = self.info.get(ips[index])
                if info_ip != "localHost" and (estados[index] in ["LISTENING", "ESTABLISHED"]):
                    string = self.printData(ips[index],info_ip)
                    print(string)
        """
        
        while True:
            try:
                time.sleep(1)
                os.system('cls')
                list_init = self.terminal.get()
                ips = list_init[self.terminal.campos[2]]
                estados = list_init[self.terminal.campos[3]]
                for index in range(len(ips)):
                    if self.info.validateIP(ips[index]) :
                        info_ip = self.info.get(ips[index], campo="ISP")
                        if info_ip != "localHost" and (estados[index] in ["LISTENING", "ESTABLISHED"]):
                            string = self.printData(ips[index],info_ip)
                            print(string)
            except (KeyboardInterrupt):
                return 
                    
        pass
    def run(self):
        
        while True:
            op = 0
            #os.system('cls')
            print("\n Consultor das conexões externas nas portas \n")
            print("   [1] - Consultar base de dados")
            print("   [2] - Ver todos os acessos")
            print("   [3] - Consulta constante dos acessos")
            print("   [4] - Sair da aplicação\n")
            opcao = input("Insira sua opção: ")
            print(opcao)

            if opcao == '1':
                self.consultaDatabase()

            elif opcao == '2':
                self.seeAllConnections()

            elif opcao == '3':
                self.continueRead()

            elif opcao == '4':
                del self.info
                return

prog = Programa()
prog.run()