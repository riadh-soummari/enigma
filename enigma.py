class Enigma:
    def __init__(self, rotors=None, rotor_positions=None, reflecteur=None, plugboard=None, notches=None):
        #une liste des rotors fréquemment utilisés qui seront proposés dans la liste déroulante 
        self.default_rotors = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
            "VZBRGITYUPSDNHLXAWMJQOFECK"   # Rotor V
        ]
        self.default_positions = [0, 1, 2]  # positions de départ par défaut des 3 rotors
        #deux reflecteurs fréquemment utilisés qui seront proposés dans une liste déroulante
        self.default_reflecteurs = {
            "Reflector B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            "Reflector C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }
        self.notches = notches or {"1": 21,"2": 4} #notches par défaut
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    #on utilise l'alphabet francais à 26 caracteres
        self.plugboard = plugboard or {}    #le plugboard peut etre laissé à vide
        self.rotors = [list(rotor) for rotor in (rotors or self.default_rotors[:3])]    #si pas spécifiés, les rotors I, II et III sont choisis
        self.rotor_positions = (rotor_positions or self.default_positions)[::-1]   #si pas spécifiées, les positions de départ par défaut seront [0, 1, 2]  
        self.reflecteur = list(reflecteur or self.default_reflecteurs["Reflector B"])   #si pas spécifié, le reflector B est utilisé par défaut

    def set_plugboard(self, plugboard_pairs): #mapping du plugboard en fonction des paires saisies au format (AB CD EF...)
        self.plugboard = {}
        for pair in plugboard_pairs:
            if len(pair) == 2 and pair[0] in self.alphabet and pair[1] in self.alphabet:
                self.plugboard[pair[0]] = pair[1]
                self.plugboard[pair[1]] = pair[0]

    def rotate_rotors(self): #rotation des rotors
        self.rotor_positions[0] = (self.rotor_positions[0] + 1) % 26
        if self.rotor_positions[0]-1 == self.notches["1"]:
            self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
        if (self.rotor_positions[0]-2 == self.notches["1"]) and (self.rotor_positions[1] == self.notches["2"]):
            self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
            self.rotor_positions[2] = (self.rotor_positions[2] + 1) % 26   
        #print(self.rotor_positions[:])   

    def encode_char(self, char): #encodage d'un caractere
        if char not in self.alphabet: #on vérifie si le caractere est connue par notre alphabet
            return char
        char = self.plugboard.get(char, char) #passage par le plugboard
        for i, rotor in enumerate(self.rotors): # passage par les rotors dans l'ordre III, II, I
            pos = self.rotor_positions[i]
            index = (self.alphabet.index(char)+pos)%26
            char = rotor[index]
            char = self.alphabet[(self.alphabet.index(char)-pos)%26]
        char = self.reflecteur[self.alphabet.index(char)]     # passage par le reflecteur
        for i, rotor in reversed(list(enumerate(self.rotors))): # parcours du chemin inverse par les rotors donc I, II, III
            pos = self.rotor_positions[i]
            index = (self.alphabet.index(char)+pos)%26
            char = self.alphabet[rotor.index(self.alphabet[index])]
            char = self.alphabet[(self.alphabet.index(char)-pos)%26]
        char = self.plugboard.get(char, char)   # 2eme passage par le plugboard
        return char # on retourne le caractere encodé

    def encode_message(self, message):  #encodage du message
        encoded_message = ""
        for char in message:    #si le caractere ne fait pas partie de notre alphabet, on l'ajoute à la chaine sans l'encoder
            if char.upper() not in self.alphabet: 
                encoded_message += char
            else:
                self.rotate_rotors()  # On déclenche la rotation à chaque itération
                encoded_message += self.encode_char(char.upper())  # On encode le caractère et on le concatène
        return encoded_message