from string import ascii_lowercase

import socket
class Enigma:
    def __init__(self, steckerbrett = {" ": " "}, alpha = None, beta=None,gama=None):
        
        self.alphabet = list(ascii_lowercase)
        self.steckerbrett = steckerbrett
        if alpha != None and beta != None and gama != None and steckerbrett != None:
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            self.alpha = alpha
            self.beta = beta
            self.gama = gama
        else: #default settings
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            rotors = [self.alpha,self.beta,self.gama]
            for rotor in rotors:
                if rotor == None or type(rotor) is not int or type(rotor) is not float:
                    rotor = 0
                else:
                    rotor = rotor % 26
            self.alpha = rotors[0]
            self.beta = rotors[1]
            self.gama = rotors[2]
        #changes in stackerbrett and set the reflector
        for letter in list(self.steckerbrett.keys()):
            if letter in self.alphabet:
                self.alphabet.remove(letter)
                self.alphabet.remove(self.steckerbrett[letter])
                self.steckerbrett.update({self.steckerbrett[letter]:letter})
            self.reflector = [leter for leter in reversed(self.alphabet)]

    def permutate(self,rotor):
        new_alphabet = ''.join(self.alphabet)
        new_alphabet = list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.insert(0,new_alphabet[-1])
            new_alphabet.pop(-1)
        #print(self.alphabet)
        #print(new_alphabet)
        return new_alphabet
    
    def inverse_permutation(self,rotor):
        new_alphabet = ''.join(self.alphabet)
        new_alphabet = list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.append(new_alphabet[0])
            new_alphabet.pop(0)
        #print(self.alphabet)
        #print(new_alphabet)
        return new_alphabet
    
    def encrypt_text(self, text):
        encrypted_text = []
        text = text.lower()
        text.split()
        for letter in text:
            if letter in self.steckerbrett:
                encrypted_text.append(self.steckerbrett[letter])
                self.alpha +=1
                if self.alpha % len(self.alphabet) == 0:
                    self.beta += 1
                    self.alpha = 0
                if self.beta %  len(self.alphabet) == 0 and self.alpha % len(self.alphabet) != 0 and self.beta >= len(
                        self.alphabet) - 1:
                    self.gama += 1
                    self.beta = 1
            else:
                # alpha -> beta -> gama -> reflector -> gama -> beta -> alpha
                temp_letter = self.permutate(self.alpha)[self.alphabet.index(letter)]
                temp_letter = self.permutate(self.beta)[self.alphabet.index(temp_letter)]
                temp_letter = self.permutate(self.gama)[self.alphabet.index(temp_letter)]
                
                temp_letter = self.reflector[self.alphabet.index(temp_letter)]

                temp_letter = self.inverse_permutation(self.gama)[self.alphabet.index(temp_letter)]
                #print("gama - {}".format(temp_letter))
                temp_letter = self.inverse_permutation(self.beta)[self.alphabet.index(temp_letter)]
                #print("beta - {}".format(temp_letter))
                temp_letter = self.inverse_permutation(self.alpha)[self.alphabet.index(temp_letter)]
                #print("alpha - {}".format(temp_letter))
                encrypted_text.append(temp_letter)
                #print(temp_letter)
                self.alpha += 1
                if self.alpha % len(self.alphabet) == 0:
                    self.beta += 1
                    self.alpha = 0
                if self.beta % len(self.alphabet) == 0 and self.alpha % len(self.alphabet) != 0 and self.beta >= len(
                        self.alphabet) - 1:
                    self.gama += 1
                    self.beta = 1
                    print('alpha - {}'.format(self.alpha))
        return ''.join(encrypted_text)
    


def main():
    text()
    ### server or client ###
    type_conn = input("Server/Client?(s/c):")
    ### read input for class Enigma ###
    alpha = int(input("alpha:"))
    beta = int(input("beta:"))
    gama = int(input("gama:"))
    steckerbrett = {}
    for i in range(3):
        in_char = input(f"{i} in_character:")
        out_char = input(f"{i} out_character:")
        steckerbrett[in_char] = out_char
    ### key encryption ###
    key = Enigma(steckerbrett=steckerbrett,alpha=alpha,beta=beta,gama=gama)
    if type_conn == 'c':
        ip = input("IP:")
        port = int(input("PORT:"))
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        while True:
            data = input("Client:")
            if data.lower() == "exit":
                break
            data = key.encrypt_text(data)
            print("Client encrypt:",data)
            s.send(data.encode())

            recv = s.recv(1024).decode()
            print("Server encrypt:",recv)
            print("Server:",key.encrypt_text(recv))

        s.close()

    elif type_conn == 's':
        ip = input("IP:")
        port = int(input("PORT:"))
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((ip,port))
        s.listen(1)
        print("Waiting...")
        conn, addr = s.accept()
        print("Connected with",addr)

        while True:
            data = conn.recv(1024).decode()
            print("Client encrypt:",data)
            data = key.encrypt_text(data)
            print("Client:",data)
            if data.lower() == 'exit':
                break
            reply = input("Server:")
            reply = key.encrypt_text(reply)
            print("Server encrypt:",reply)
            conn.send(reply.encode())
        conn.close()

    

def text():
    print("#"*15)
    print("# ENIGMA CHAT #")
    print("#"*15)
    


if __name__ == '__main__':
    main()




