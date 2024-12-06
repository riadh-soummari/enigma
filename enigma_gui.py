import tkinter as tk
from tkinter import ttk, messagebox
from enigma import Enigma


class EnigmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enigma")
        self.enigma = Enigma()
        self.root.configure(bg='#2A2A2A')
        # champ pour la saisie du message
        tk.Label(root, text="Message:", fg="yellow", bg="#2A2A2A", font=("Arial", 12, "bold")).grid(row=0, column=0)
        self.message_entry = tk.Text(root, width=60, height=5, font=("Arial", 10))
        self.message_entry.grid(row=0, column=1, columnspan=2, pady=10)
        # 3 listes déroulantes pour le choix des 3 rotors contenant les 6 rotors par défaut et possibilité de saisir rotors custom
        tk.Label(root, text="Rotors:", fg="white", bg="#2A2A2A", font=("Arial", 11, "bold")).grid(row=1, column=0)
        self.rotor1_combo = self.create_rotor_dropdown(1)
        self.rotor2_combo = self.create_rotor_dropdown(2)
        self.rotor3_combo = self.create_rotor_dropdown(3)
        # champ pour la saisie des notches
        tk.Label(root, text="Notches: (0-25) ", fg="white", bg="#2A2A2A", font=("Arial", 10, "bold")).grid(row=2, column=0)
        self.notches_entry = tk.Entry(root, width=20, font=("Arial", 10))
        self.notches_entry.insert(0, "21,4") 
        self.notches_entry.grid(row=2, column=1, pady=10)
        # champ pour la saisie des positions de départ au format "0,1,2"
        tk.Label(root, text="Positions de départ: (0-25) ", fg="white", bg="#2A2A2A", font=("Arial", 10, "bold")).grid(row=3, column=0)
        self.position_entry = tk.Entry(root, width=20, font=("Arial", 10))
        self.position_entry.insert(0, "0,1,2")  
        self.position_entry.grid(row=3, column=1, pady=10)
        # liste déroulante pour choix du reflecteur et possibilité de saisir reflecteur custom
        tk.Label(root, text="Reflecteur:", fg="white", bg="#2A2A2A", font=("Arial", 11, "bold")).grid(row=4, column=0)
        self.reflector_combo = ttk.Combobox(root, width=30, font=("Arial", 8))
        self.reflector_combo['values'] = list(self.enigma.default_reflecteurs.values())
        self.reflector_combo.insert(0, "YRUHQSLDPXNGOKMIEBFZCWVJAT")  # Reflector B est choisi par défaut
        self.reflector_combo.grid(row=4, column=1, pady=10)
        self.reflector_label = tk.Label(root, fg="lightgreen", bg="#2A2A2A", text="Reflector B", font=("Arial", 12, "bold"))
        self.reflector_label.grid(row=4, column=2, padx=5, pady=10, sticky="w")
        #champ pour saisie du plugboard
        tk.Label(root, text="Plugboard: (AB CD EF) ", fg="white", bg="#2A2A2A", font=("Arial", 10, "bold")).grid(row=5, column=0)
        self.plugboard_entry = tk.Entry(root, width=60, font=("Arial", 10))
        self.plugboard_entry.grid(row=5, column=1, columnspan=2, pady=10)
        #bouton pour encode
        self.encode_button = tk.Button(root, text="Encode", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.encode_message)
        self.encode_button.grid(row=6, column=0, columnspan=4, pady=15)
        #message encodé
        tk.Label(root, text="Message encodé: ", fg="yellow", bg="#2A2A2A", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2)
        self.encoded_message = tk.Text(root, width=60, height=5, font=("Arial", 10))
        self.encoded_message.grid(row=7, column=1, columnspan=3, pady=10)
        #bouton pour réinitialiser les rotors aux positions initiales
        self.reset_button = tk.Button(root, text="Revenir aux positions de départ", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.reset_machine)
        self.reset_button.grid(row=8, column=0, columnspan=4, pady=15)
        #mise à jour du libellé du reflecteur choisi
        self.reflector_combo.bind("<<ComboboxSelected>>", self.update_reflector_label)

    #création des listes deroulantes pour choix des rotors avec la possibilité de choisir parmis les 5 rotors par defaut
    def create_rotor_dropdown(self, rotor_number):
        combo = ttk.Combobox(self.root, width=30, font=("Arial", 8))
        combo['values'] = self.enigma.default_rotors 
        combo.insert(0, self.enigma.default_rotors[rotor_number - 1]) 
        combo.grid(row=1, column=rotor_number, padx=5, pady=10)
        return combo
        
    #mise à jour du libellé du reflecteur choisi
    def update_reflector_label(self, event=None):
        self.reflector_label.config(text="")
        selected_reflector_string = self.reflector_combo.get()
        for label, wiring in self.enigma.default_reflecteurs.items():
            if wiring == selected_reflector_string:
                self.reflector_label.config(text=f"{label}")

    def encode_message(self):
        try:
            # Vérification de la validité des rotors
            rotors = [
                list(self.rotor3_combo.get()),
                list(self.rotor2_combo.get()),
                list(self.rotor1_combo.get())
            ]
            for rotor in rotors:
                if len(rotor) != 26 or any(c not in self.enigma.alphabet for c in rotor):
                    tk.messagebox.showerror("Erreur", "Les rotors doivent contenir exactement 26 lettres de l'alphabet.")
                    return
            self.enigma.rotors = rotors
            # Vérification de la validité des notches
            notch_input = self.notches_entry.get().split(',')
            if len(notch_input) != 2 or not all(notch.isdigit() and 0 <= int(notch) <= 25 for notch in notch_input):
                tk.messagebox.showerror("Erreur", "Les notches doivent être deux nombres entre 0 et 25, séparés par une virgule.")
                return
            notches = {
                "1": int(notch_input[0]),
                "2": int(notch_input[1]),
            }
            self.enigma.notches = notches
            # Vérification de la validité du reflecteur
            selected_reflector = self.reflector_combo.get()
            if len(selected_reflector) != 26 or any(c not in self.enigma.alphabet for c in selected_reflector):
                tk.messagebox.showerror("Erreur", "Le reflecteur doit contenir exactement 26 lettres de l'alphabet.")
                return
            self.enigma.reflecteur = selected_reflector
            # Vérification des positions initiales
            if not hasattr(self, "positions_initialized") or not self.positions_initialized:
                initial_positions = self.position_entry.get().split(',')
                if len(initial_positions) != 3 or not all(pos.isdigit() and 0 <= int(pos) <= 25 for pos in initial_positions):
                    tk.messagebox.showerror("Erreur", "Les positions initiales doivent être trois nombres entre 0 et 25, séparés par des virgules.")
                    return
                self.enigma.rotor_positions = [int(pos) for pos in initial_positions][::-1]
                self.positions_initialized = True  # marqueur pour indiquer que les positions initiales ont été configurées et donc qu'on les réinitialise pas à chaque encodage
            # Vérification du plugboard
            plugboard_input = self.plugboard_entry.get().split()
            for pair in plugboard_input:
                if len(pair) != 2 or any(char.upper() not in self.enigma.alphabet for char in pair):
                    tk.messagebox.showerror("Erreur", "Le plugboard doit être au format AB CD EF, avec des lettres valides de l'alphabet.")
                    return
            plugboard_pairs = [tuple(pair.upper()) for pair in plugboard_input]
            self.enigma.set_plugboard(plugboard_pairs)

            # récuperation du message saisi avec suppression des espaces inutiles
            message = self.message_entry.get("1.0", tk.END).strip() 
            encoded_message = self.enigma.encode_message(message)
            self.encoded_message.delete("1.0", tk.END) 
            self.encoded_message.insert("1.0", encoded_message) 

        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite : {e}")

    def reset_machine(self):
        #bouton pour réinitialiser les rotors aux positions initiales
        initial_positions = self.position_entry.get().split(',')
        if len(initial_positions) != 3 or not all(pos.isdigit() and 0 <= int(pos) <= 25 for pos in initial_positions):
            tk.messagebox.showerror("Erreur", "Les positions initiales doivent être trois nombres entre 0 et 25, séparés par des virgules.")
            return
        self.enigma.rotor_positions = [int(pos) for pos in initial_positions][::-1]
        self.positions_initialized = False
        self.encoded_message.delete("1.0", tk.END)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop() 