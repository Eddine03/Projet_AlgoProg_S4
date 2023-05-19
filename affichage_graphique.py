import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.filedialog as tfd
from tkinter import ttk
import csv
from random import randint
from math import sqrt,ceil
import copy
from Labyrinthe import *

class Fenetre():
    """
    Cette classe sert à paramétrer la fenêtre d'affichage de notre programme. Elle contient toutes les fonctions qui gèrent l'affichage graphique de la fenêtre principale.
    """
    def __init__(self, root= None, methode = None):
        self.racine = tk.Tk()
        self.racine.title("Labyrotron 2023")
        self.racine.configure(bg='lightblue')
        self.width = 600 # taille du canevas en x et en y
        self.height = 600 
        self.scale_min = 2 # valeur minimale et maximale de la taille de labyrinthe
        self.scale_max = 100 
        self.size_cell_x=10 # taille d'une case du labyrinthe en x et en y
        self.size_cell_y=10 
        self.color={'wall':'black','path':'white','start':'green','end':'red'} # les relations entre les blocs de notre labyrinthe et leurs couleurs correspondantes

        self.width_var = tk.IntVar() # valeur de la scalebar pour la taille x
        self.height_var = tk.IntVar() # valeur de la scalebar pour la taille y
        self.width_var.set(10) # on initialise les 2 variables a 10 (labyrinthe 10x10)
        self.height_var.set(10)
        self.outil = tk.StringVar() # string de la méthode a utiliser pour colorier le labyrinthe
        self.outil.set("Ligne droite")
        self.x1 = 0 # position x et y d'un point sur le canevas
        self.y1 = 0

        self.creer_widgets_main(self.racine)
        self.initialisation()
  
    def creer_widgets_main(self,root):
        """
        Fonction qui crée toutes les widgets de la fenêtre principale, gère leurs affectations de fonctions et les place au bon endroit sur la fenêtre graphique.

        Input :
            root : la fenêtre principale de notre affichage
        """
        self.cadre_labyrinthe = tk.Frame(root, padx=10, pady=10, bg='lightblue')
        self.cadre_labyrinthe.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.cadre_labyrinthe,width = self.width, height = self.height, bg='lightblue', highlightthickness=0)
        self.canvas.pack(fill='both')
        


        self.cadre_sauvegarde = tk.Frame(root, padx=10, pady=10, bg='lightpink')
        self.cadre_sauvegarde.pack(side=tk.TOP, fill='x')

        self.label_sauvegarde = tk.Label(self.cadre_sauvegarde, text='Sauvegarde', bg='lightpink', font=('Comic Sans MS', 10, 'bold'))
        self.label_sauvegarde.pack(side=tk.TOP, fill='x')

        self.bouton_1 = tk.Button(self.cadre_sauvegarde, text="Importer un labyrinthe")
        self.bouton_1.bind('<Button-1>',self.import_labyrinthe)
        self.bouton_1.pack(fill = 'x', side=tk.TOP)
        
        self.bouton_2 = tk.Button(self.cadre_sauvegarde, text="Exporter ce labyrinthe")
        self.bouton_2.bind('<Button-1>',self.export_labyrinthe)
        self.bouton_2.pack(fill = 'x', side=tk.TOP)
        


        self.cadre_resolution = tk.Frame(root, padx=10, pady=10, bg='yellow')
        self.cadre_resolution.pack(side=tk.TOP, fill='x')

        self.label_resolution = tk.Label(self.cadre_resolution, text='Résolution', bg='yellow', font=('Comic Sans MS', 10, 'bold'))
        self.label_resolution.pack(side=tk.TOP, fill='x')

        self.algo = ttk.Combobox(self.cadre_resolution, values=['BFS','DFS','A*','Les trois'],state='readonly')
        self.algo.pack(fill='x')
        self.algo.current(0)
        
        self.bouton_4 = tk.Button(self.cadre_resolution, text="Résoudre")
        self.bouton_4.bind('<Button-1>',self.solve)
        self.bouton_4.pack(fill = 'x', side=tk.TOP)
        


        self.cadre_generation = tk.Frame(root, padx=10, pady=10, bg='lightgreen')
        self.cadre_generation.pack(fill='x', side=tk.TOP)

        self.label_generation = tk.Label(self.cadre_generation, text='Génération', bg='lightgreen', font=('Comic Sans MS', 10, 'bold'))
        self.label_generation.pack(side=tk.TOP, fill='x')

        self.width_scale = tk.Scale(self.cadre_generation, orient='horizontal', 
                                        from_= self.scale_min, 
                                        to = self.scale_max,
                                        resolution=1, 
                                        tickinterval=19, label='Taille X', variable = self.width_var)
        self.width_scale.pack(side="top", fill='x')

        self.height_scale = tk.Scale(self.cadre_generation, orient='horizontal', 
                                        from_= self.scale_min, 
                                        to = self.scale_max,
                                        resolution=1, 
                                        tickinterval=19, label='Taille Y', variable = self.height_var)
        self.height_scale.pack(side="top", fill='x')

        self.bouton_3 = tk.Button(self.cadre_generation, text="Générer un labyrinthe")
        self.bouton_3.bind('<Button-1>',self.generate_labyrinthe)
        self.bouton_3.pack(fill = 'x', side=tk.TOP)
        
        self.init_button = tk.Button(self.cadre_generation,text="Générer un cadre vide")
        self.init_button.bind('<Button-1>',self.initialisation)
        self.init_button.pack(fill = 'x', side=tk.TOP)
        


        self.cadre_edition = tk.Frame(root, padx=10, pady=10, bg='lightgrey')
        self.cadre_edition.pack(fill='x', side=tk.TOP)

        self.label_edition = tk.Label(self.cadre_edition, text='Edition', bg='lightgrey', font=('Comic Sans MS', 10, 'bold'))
        self.label_edition.pack(side=tk.TOP, fill='x')

        self.couleur = ttk.Combobox(self.cadre_edition, values=list(self.color.keys()),state='readonly')
        self.couleur.pack(fill='x')
        self.couleur.current(0)
        
        self.outil_1 = tk.Radiobutton(self.cadre_edition,text="Main levée",variable=self.outil,value="Main levée")
        self.outil_1.pack(fill='x')
        self.outil_2 = tk.Radiobutton(self.cadre_edition,text="Ligne droite",variable=self.outil,value="Ligne droite")
        self.outil_2.pack(fill='x')

        self.bouton_5 = tk.Button(self.cadre_edition, text="Effacer l'affichage")
        self.bouton_5.bind('<Button-1>',self.clear)
        self.bouton_5.pack(fill = 'x', side=tk.TOP)

    def initialisation(self,event=None):
        """
        Fonction qui initialise le labyrinthe en fonction de la taille de labyrinthe que l'utilisateur choisit avec les scalebars.
        """
        self.delete_all()
        self.labyrinthe = Labyrinthe()
        self.size_cell_x = int(self.width / self.width_var.get())
        self.size_cell_y = int(self.height / self.height_var.get())
        for id_y in range(self.height_var.get()):
            self.labyrinthe.grid.append([])
            for id_x in range(self.width_var.get()):
                case=Case([(id_x,id_y),"path"])
                self.labyrinthe.grid[id_y].append(case)
                case.pixel_id = self.canvas.create_rectangle(case.coordinates[0]*self.size_cell_x,case.coordinates[1]*self.size_cell_y,(case.coordinates[0]+1)*self.size_cell_x,(case.coordinates[1]+1)*self.size_cell_y,width=0, fill=self.color[case.type])
                self.canvas.tag_bind(case.pixel_id,'<Button-1>',self.edit_start)
                self.canvas.tag_bind(case.pixel_id,'<ButtonRelease-1>',self.edit_end)
        self.labyrinthe.size=(self.height_var.get(),self.width_var.get())
        self.labyrinthe.assign_neighbor()
        
                
    def delete_all(self) :
        """
        Fonction qui supprime tous les éléments du canevas.
        """
        for i in self.canvas.find_all() :
            self.canvas.delete(i)
        
 
    def import_labyrinthe(self,event) :
        """
        Fonction qui permet d'importer un labyrinthe au format CSV puis de l'afficher sur notre canevas.
        """
        url = tfd.askopenfilename(filetypes=[('csv file','*.csv')],defaultextension='csv')
        good_import=True
        try :
            new_labyrinthe = Labyrinthe()
            new_labyrinthe.import_(url)
        except :
            good_import=True
        if good_import :
            self.delete_all()
            self.labyrinthe = new_labyrinthe

            self.size_cell_x = int(self.width / self.labyrinthe.size[1])
            self.size_cell_y = int(self.height / self.labyrinthe.size[0])
            for i in self.labyrinthe.grid:
                for case in i:
                    case.pixel_id=self.canvas.create_rectangle(case.coordinates[0]*self.size_cell_x,case.coordinates[1]*self.size_cell_y,(case.coordinates[0]+1)*self.size_cell_x,(case.coordinates[1]+1)*self.size_cell_y,width=0, fill=self.color[case.type])
                    self.canvas.tag_bind(case.pixel_id,'<Button-1>',self.edit_start)
                    self.canvas.tag_bind(case.pixel_id,'<ButtonRelease-1>',self.edit_end)


    
    def export_labyrinthe(self,event) :
        """
        Fonction qui permet d'exporter notre labyrinthe au format CSV en choissisant un nom stylé.
        """
        url = tfd.asksaveasfilename(filetypes=[('csv file','*.csv')], initialfile=f"labyrinthe_{self.labyrinthe.size[0]}x{self.labyrinthe.size[1]}.csv", defaultextension='csv')
        self.labyrinthe.export(url)

    
    def generate_labyrinthe(self,event):
        """
        Fonction génère un labyrinthe aléatoirement avec l'algortihme de prim et l'affiche. 
        """
        grille = self.prim()
        self.delete_all()
        self.labyrinthe = Labyrinthe()
        self.size_cell_x = int(self.width / self.width_var.get())
        self.size_cell_y = int(self.height / self.height_var.get())
        for y in range (len(grille)):
            self.labyrinthe.grid.append([])
            for x in range (len(grille[y])):
                case=Case([(x,y),f"{grille[y][x]}"])
                self.labyrinthe.grid[y].append(case)
                case.pixel_id = self.canvas.create_rectangle(case.coordinates[0]*self.size_cell_x,case.coordinates[1]*self.size_cell_y,(case.coordinates[0]+1)*self.size_cell_x,(case.coordinates[1]+1)*self.size_cell_y,width=0, fill=self.color[case.type])
                self.canvas.tag_bind(case.pixel_id,'<Button-1>',self.edit_start)
                self.canvas.tag_bind(case.pixel_id,'<ButtonRelease-1>',self.edit_end)
        while self.labyrinthe.start == None :
            x, y = randint(0, ceil((self.width_var.get()-1)/2)), randint(0, ceil((self.height_var.get()-1)/2))
            case = self.labyrinthe.grid[y][x]
            if case.type == "path" :
                case.type = "start"
                self.labyrinthe.start = case
                self.canvas.itemconfigure(case.pixel_id, fill=self.color[case.type]) 
        while self.labyrinthe.end == None :
            x, y = randint(int((self.width_var.get()-1)/2), self.width_var.get()-1), randint(int((self.height_var.get()-1)/2), self.height_var.get()-1)
            case = self.labyrinthe.grid[y][x]
            if case.type == "path" :
                case.type = "end"
                self.labyrinthe.end = case
                self.canvas.itemconfigure(case.pixel_id, fill=self.color[case.type]) 
            
            
        self.labyrinthe.size=(self.height_var.get(),self.width_var.get())
        self.labyrinthe.assign_neighbor()

    def initialiser_grille(self):
        """
        Fonction qui crée une grille de labyrinthe remplit de mur.

        Output : 
            grille : matrice, grille du labyrinthe généré
        """
        return [["wall" for x in range(self.width_var.get())] for y in range(self.height_var.get())]

    def est_dans_grille(self,x,y):
        """
        Fonction qui vérifie si la cellule fait bien parti de la grille du labyrinthe.

        Input :
            x : entier, position x de la cellule
            y : entier, position y de la cellule

        Output : 
            condition : True or False, condition de présence de la cellule dans la grille
        """
        return 0 <= x < self.width_var.get() and 0 <= y < self.height_var.get()

    def voisins(self,x,y):
        """
        Fonction qui renvoie les voisins d'une cellule

         Input :
            x : entier, position x de la cellule
            y : entier, position y de la cellule

        Output : 
            liste_voisins : liste, liste des voisins de la cellule
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return [(x+dx, y+dy) for dx, dy in directions if self.est_dans_grille(x+dx,y+dy)]

    def prim(self):
        """
        Fonction génère un labyrinthe aléatoirement avec l'algortihme de prim.

        Output :
            grille : matrice, grille du labyrinthe généré
        """
        grille = self.initialiser_grille()
        x, y = randint(0, self.width_var.get()-1), randint(0, self.height_var.get()-1)
        grille[y][x] = 'path'
        frontiere = self.voisins(x, y)
        while frontiere:
            x, y = frontiere.pop(randint(0, len(frontiere)-1))
            voisins_vide = [n for n in self.voisins(x,y) if grille[n[1]][n[0]] == 'path']
            if len(voisins_vide) == 1:
                grille[y][x] = 'path'
                frontiere.extend(n for n in self.voisins(x,y) if grille[n[1]][n[0]] == 'wall')
        return grille
       
    def solve(self,event) :
        """
        Fonction qui lance la résolution du labyrinthe par les différents algorithmes disponible en fonction de ce que l'utilisateur décide.
        """
        if self.labyrinthe.start is not None and self.labyrinthe.end is not None:
            if self.algo.get()=='Les trois':
                Fenetre_animation(self.labyrinthe,self.racine,'A*',self.size_cell_x,self.size_cell_y)
                Fenetre_animation(self.labyrinthe,self.racine,'BFS',self.size_cell_x,self.size_cell_y)
                Fenetre_animation(self.labyrinthe,self.racine,'DFS',self.size_cell_x,self.size_cell_y)
            else :
                Fenetre_animation(self.labyrinthe,self.racine,self.algo.get(),self.size_cell_x,self.size_cell_y)

    
    def clear(self,event) :
        """
        Fonction qui efface le labyrinthe actuel en repeignant en blanc toutes les cases.
        """
        self.couleur.set("path")
        for pixel_id in self.canvas.find_all():
            if self.canvas.itemcget(pixel_id, "fill") != "white" :
                case = self.labyrinthe.get_case_from_id(pixel_id)
                if case.type == "start" :
                    self.labyrinthe.start = None
                if case.type == "end" :
                    self.labyrinthe.end = None
                case.type = self.couleur.get()
                self.canvas.itemconfigure(pixel_id, fill=self.color[case.type])
        self.couleur.set("wall")   
        

    def edit_start(self,event):
        """
        Fonction qui permet à l'utilisateur de modifier le labyrinthe en fonction de la couleur choisie et du mode de dessin sélectionné. Elle correspond au clic de souris gauche.
        """
        if self.couleur.get() == "start" and self.labyrinthe.start == None :
            self.draw_pixel(int(self.canvas.canvasx(event.x)),int(self.canvas.canvasy(event.y)))

        elif self.couleur.get() == "end" and self.labyrinthe.end == None :
            self.draw_pixel(int(self.canvas.canvasx(event.x)),int(self.canvas.canvasy(event.y)))
            
        elif self.outil.get() == "Ligne droite" and (self.couleur.get() != "start" and self.couleur.get() != "end") :
            self.x1 = int(self.canvas.canvasx(event.x))
            self.y1 = int(self.canvas.canvasy(event.y))
        
        elif self.outil.get() == "Main levée" and (self.couleur.get() != "start" and self.couleur.get() != "end"):
            self.canvas.bind('<Motion>',self.draw_hand)

    
    def edit_end(self,event):
        """
        Fonction qui permet à l'utilisateur de modifier le labyrinthe en fonction de la couleur choisie et du mode de dessin sélectionné. Elle correspond au clic de souris droit.
        """
        if self.couleur.get() != "start" and self.couleur.get() != "end":
            if self.outil.get() == "Ligne droite" :
                x2 = int(self.canvas.canvasx(event.x))
                y2 = int(self.canvas.canvasy(event.y))
                if self.x1 <= x2 :
                    self.draw_ligne(self.x1,self.y1,x2,y2)
                else :
                    self.draw_ligne(x2,y2,self.x1,self.y1)
                self.x1 = 0
                self.y1 = 0
            elif self.outil.get() == "Main levée" :
                for pixel_id in self.canvas.find_all():
                    self.canvas.unbind('<Motion>')

    
    def draw_ligne(self,x1,y1,x2,y2):
        """
        Fonction qui trace une ligne droite entre 2 points défini par les 2 clics de souris.

        Input :
            x1 : entier, position x du point sélectionné le plus à gauche sur le canevas
            y1 : entier, position y du point sélectionné le plus à gauche sur le canevas
            x2 : entier, position x du 2ème point selectionné
            y2 : entier, position y du 2ème point selectionné
        """
        dx = x2-x1
        dy = y2-y1
        if dx <= self.size_cell_x :
            if dy == 0 :
                self.draw_pixel(x1,y1)
            elif dy > 0 :
                for y in range(y1,y2):
                    self.draw_pixel(x1,y)
            else :
                for y in range(y1,y2,-1):
                    self.draw_pixel(x1,y)
        else :
            pente = dy/dx 
            for x in range(x1,x2):
                y = round(pente*(x-x1)+y1)
                self.draw_pixel(x,y)
        self.draw_pixel(x2,y2)

    
    def draw_hand(self,event):
        """
        Fonction qui récupère les coordonnées de la souris pour le dessin à main levée. 
        """
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        self.draw_pixel(x,y)

    
    def draw_pixel(self,x,y):
        """
        Fonction qui change la couleur de la case la plus proche d'une position (x,y) sur le canevas.

        Input :
            x : entier, position x du point 
            y : entier, position y du point
        """
        pixel_id = self.canvas.find_closest(x,y)
        case = self.labyrinthe.get_case_from_id(pixel_id[0])
        newtype = self.couleur.get()
        if case.type!=newtype:
            if case.type == "start" :
                self.labyrinthe.start = None
            elif case.type == "end" :
                self.labyrinthe.end = None
            case.type = newtype
            if case.type == "start" :
                self.labyrinthe.start = case
            elif case.type == "end" :
                self.labyrinthe.end = case
            self.labyrinthe.sequence_affichage={'BFS':[],'DFS':[],'A*':[]}
        self.canvas.itemconfigure(pixel_id,fill=self.color[case.type])
        
            
            
class Fenetre_animation(tk.Toplevel):
    """
    Cette classe a paramétrer la fenêtre d'animation de résolution du labyrinthe par les différents algorithmes.
    """
    def __init__(self,labyrinthe,racine,algo,size_cell_x,size_cell_y):
        super().__init__(racine) # initialisation de la fenêtre par héritage de l'initialisation d'un tk.Toplevel
        self.title(f"Résolution par {algo}")
        self.labyrinthe=labyrinthe
        self.racine=racine
        self.algo=algo
        self.configure(bg='lightblue')

        self.size_cell_x = size_cell_x # taille d'une case du labyrinthe en x et en y
        self.size_cell_y = size_cell_y
        self.width=labyrinthe.size[0]*self.size_cell_y
        self.height=labyrinthe.size[1]*self.size_cell_x
        #self.geometry(f"{int(self.width)}x{int(self.height)}")
        self.color={'wall':'black','path':'white','start':'green','end':'red','explored':'orange','identified':'yellow','solution':'#20A1D4'} # les relations entre les blocs de notre labyrinthe et leurs couleurs correspondantes
        self.animation_step=0 # compteur qui gère a quel moment de l'animation nous nous trouvons

        self.canvas=tk.Canvas(self, height=self.height, width=self.width, bg='lightblue', highlightthickness=0)
        self.canvas.pack(fill='both', padx=30, pady=30)

        self.build_lab()

    def build_lab(self):
        """
        Fonction qui recréer le labyrinthe dans la nouvelle fenêtre.
        """
        for i in self.labyrinthe.grid:
            for case in i:
                case.animation_pixel_id=self.canvas.create_rectangle(case.coordinates[0]*self.size_cell_x,case.coordinates[1]*self.size_cell_y,(case.coordinates[0]+1)*self.size_cell_x,(case.coordinates[1]+1)*self.size_cell_y,width=0, fill=self.color[case.type])
        # on regarde s'il n'y a pas deja une séquence d'affichage qui existe pour ce labyrinthe
        if self.algo=='BFS' and len(self.labyrinthe.sequence_affichage['BFS'])==0: 
            self.labyrinthe.solving_BFS()
        elif self.algo=='DFS'and len(self.labyrinthe.sequence_affichage['DFS'])==0:
            self.labyrinthe.solving_DFS()
        elif self.algo=="A*" and len(self.labyrinthe.sequence_affichage['A*'])==0:
            self.labyrinthe.solving_A_star()
        self.sequence_affichage=self.labyrinthe.sequence_affichage[self.algo] 
        self.duree = 10000//len(self.sequence_affichage)
        self.animate()
        
    def animate(self):
        """
        Fonction qui anime la résolution de notre labyrinthe en temps réel. L'animation prends 10 secondes puis on affiche le chemin final pendant 2 secondes avant de réafficher l'animation de résolution.
        """
        if self.canvas.winfo_exists():
            sequence=self.sequence_affichage[self.animation_step]
            for cell_id, newstate in sequence:
                self.canvas.itemconfig(cell_id,fill=self.color[newstate])
            self.animation_step+=1
            if self.animation_step==len(self.sequence_affichage):
                self.animation_step=0
            if self.animation_step==len(self.sequence_affichage)-1:
                self.racine.after(2000+10000%len(self.sequence_affichage),self.animate)
            else:
                self.racine.after(self.duree,self.animate)        

if __name__ == "__main__":
    app = Fenetre()
    app.racine.mainloop()
