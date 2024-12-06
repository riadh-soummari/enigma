# Machine Enigma à 3 rotors

## Fonctionnalités

- **Configuration des rotors** : Possibilité de choisir parmi 5 rotors proposés ou de saisir un rotor personnalisé.
- **Modifier les positions initiales** : Saisir au format `x,y,z` où `x, y, z` vont de 0 à 25.
- **Modifier les notches des rotors** : Saisir au format `x,y` où `x, y` vont de 0 à 25.
- **Configuration du réflecteur** : Possibilité de choisir parmi 2 réflecteurs proposés ou de saisir un réflecteur personnalisé.
- **Configuration du Plugboard** : Possibilité de définir un plugboard pour permuter les paires de lettres, saisir au format `AB CD EF ...`.
- **Interface graphique** : Réalisée avec la bibliothèque **Tkinter**.
- **Bouton retour aux positions de départ** : Permet de réinitialiser les rotors aux positions initiales pour décoder un message encodé.

---

## Configuration de base

Par défaut, la machine Enigma est configurée comme suit :

### Rotor 1
- **Câblage** : `EKMFLGDQVZNTOWYHXUSPAIBRCJ` (Rotor I)
- **Notch** : 0
- **Position initiale** : 0

### Rotor 2
- **Câblage** : `AJDKSIRUXBLHWTMCQGZNPYFVOE` (Rotor II)
- **Notch** : 4
- **Position initiale** : 1

### Rotor 3
- **Câblage** : `BDFHJLCPRTXVZNYEIWGAKMUSQO` (Rotor III)
- **Notch** : 21
- **Position initiale** : 2

### Réflecteur
- **Câblage** : `YRUHQSLDPXNGOKMIEBFZCWVJAT` (Reflector B)

### Plugboard
- **Configuration par défaut** : Aucune permutation (vide).

---

## Lancer l'interface graphique Enigma

- **Version de python utilisée** : 3.12


```bash
python enigma_gui.py
