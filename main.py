import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import csv
import random
from math import sqrt

class Fenetre_avec_graphique():
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Main window")
        self.width = 2000
        self.height = 2000

        self.epaisseur_min = 10
        self.epaisseur_max = 100

        self.colors = ['Red','Blue','Green','Magenta']

        self.outil = 0

        self.creer_widgets(self.racine)
    def creer_widgets(self,root):
        self.canva = tk.Canvas(root, bg='lightyellow')
        self.canva.pack(side=tk.LEFT, fill='y')

        self.bouton_1 = tk.Button(root, text="Importer un labyrinthe")
        self.bouton_1.pack(fill = 'x', side=tk.TOP)

        self.bouton_2 = tk.Button(root, text="Exporter ce labyrinthe")
        self.bouton_2.pack(fill = 'x', side=tk.TOP)

        self.bouton_3 = tk.Button(root, text="Résoudre")
        self.bouton_3.pack(fill = 'x', side=tk.TOP)

        self.bouton_4 = tk.Button(root, text="Effacer l'affichage")
        self.bouton_4.pack(fill = 'x', side=tk.TOP)

        self.epaisseur_scale = tk.Scale(root, orient='horizontal', 
                                        from_= self.epaisseur_min, 
                                        to = self.epaisseur_max,
                                        resolution=10, 
                                        tickinterval=25, length=130, label='Epaisseur')
        self.epaisseur_scale.pack()

        self.couleur = ttk.Combobox(root, values=self.colors)
        self.couleur.pack(fill='x')
        self.couleur.current(1)


        self.outil_1 = tk.Radiobutton(root,text="Main levée",variable=self.outil)
        self.outil_1.pack()
        self.outil_2 = tk.Radiobutton(root,text="Ligne droite",variable=self.outil)
        self.outil_2.pack()
        self.outil_3 = tk.Radiobutton(root,text="Remplir",variable=self.outil)
        self.outil_3.pack()



if __name__ == "__main__":
    app = Fenetre_avec_graphique()
    app.racine.mainloop()
