import os

class ReaderTerminal:

    def __init__(self, element=None, numerLine=None, system = 'windows'):
        self.element = element
        self.numberLine = numerLine
        self.sys = system
        self.dataDict = None
        
        pass

    def __removeSpace(self, str):
        copy = []
        index = 0
        for char in str:
            if not ((char == ' ' and index == 0) or (char == '\n')):
                copy += char
            index += 1
        
        return ''.join(copy)

    def __getCampos(self, line):
        index = 0
        param = line.split('  ')
        campos = []
        for pos in param:
            if pos != '':
                campos.append(self.__removeSpace(pos))
        print(campos)
        return campos
    
    def __readTerminal(self):
        
        if self.sys == 'windows':
            os.system("netstat -na  > netstat.log.tmp")
        
        file = open("netstat.log.tmp", 'r')
        self.arquivo = file.readlines()
        file.close()
        os.remove('netstat.log.tmp')
        pass

    def __calcPosition(self):
        self.positon = {}
        tam = len(self.campos)
        index = 0
        for campo in self.campos :
            if index == (tam-1):
                aux = [self.enum.rfind(self.campos[tam-1]),self.enum.rfind('\n')]
                self.positon[campo] =  [aux[0],aux[1], aux[1]-aux[0]]
            else:
                aux = [self.enum.rfind(self.campos[index]),self.enum.rfind(self.campos[index+1])]
                self.positon[campo] =  [aux[0],aux[1], aux[1]-aux[0]]
            index +=1
        print(self.positon)

    def __getPosition(self, position):
        tam = len(self.campos)
        if position == (tam-1):
            return self.enum.rfind(self.campos[tam-1]),self.enum.rfind('\n')
        else:
            return self.enum.rfind(self.campos[position]),self.enum.rfind(self.campos[position+1])
    
    def get(self):
        self.__readTerminal()
        index = 0
        get = 0
        self.dataDict = {}
        for line in self.arquivo:
            if get == 1:
                index = 0
                for campo in self.campos :
                    #pos_init,pos_end = self.__getPosition(index)
                    #self.dataDict[campo].append(line[pos_init:pos_end])
                    pos= self.positon[campo]
                    if index == len(self.campos)-1:
                        aux = line[pos[0]:] if line[pos[0]:] != '\n' else ' '
                        param = aux.split('\n');
                        self.dataDict[campo].append(param[0])
                    else:
                        self.dataDict[campo].append(line[pos[0]:pos[1]])
                    index += 1            

            elif ((line.count(self.element) > 0 and self.element != None) or (self.numberLine == index and self.numberLine != None)) and get == 0:
                get = 1
                self.enum = line
                self.campos = self.__getCampos(line)
                for campo in self.campos :
                    self.dataDict[campo] = []
                self.__calcPosition()
        
        return self.dataDict
    
    def show(self):
        if self.dataDict == None:
            self.get()

        string = ""
        index = 0
        for campo in self.campos :
            if index == len(self.campos)-1:
                vet = self.positon[campo]
                string += "{}".format(campo)
            else:
                vet = self.positon[campo]
                camp = "{:"+str("{}".format(vet[2])) + "}|"
                string += camp.format(campo)
            index +=1
        print(string)
        
        for index in range(len(self.dataDict[self.campos[0]])):
            string_body = ""
            jndex = 0
            for campo in self.campos :
                if jndex == len(self.campos)-1:
                    dado = self.dataDict[campo]
                    string_body += "{}".format(dado[index])
                else:
                    vet = self.positon[campo]
                    camp = "{:"+str("{}".format(vet[2])) + "}|"
                    dado = self.dataDict[campo]
                    string_body += camp.format(dado[index])
                jndex +=1
                
            print(string_body)
        pass

#ips = ReaderTerminal(element="externo")
#print(ips.get())
#ips.show()