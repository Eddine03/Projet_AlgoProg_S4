import csv
from ast import literal_eval
from queue import PriorityQueue
from math import sqrt

class Labyrinthe:
    """
    Cette classe sert à paramétrer le labyrinthe que l'on veut résoudre. Elle contient toutes les fonctions qui gèrent le bon fonctionnement du labyrinthe et de sa résolution.
    """
    def __init__(self):
        self.grid=[]
        self.size=None
        self.start=None
        self.end=None
        self.sequence_affichage={'DFS':[],'BFS':[],'A*':[]}

    def import_(self, url):
        """
        Fonction qui crée un labyrinthe à partir d'un fichier csv.

        Input :
            url : string, url du fichier csv à traiter
        """
        with open(url,'r',encoding='utf-8') as file:
            csvReader=csv.reader(file,delimiter=';')
            self.grid=[[Case(literal_eval(csv_data)) for csv_data in row] for row in csvReader if len(row)]
        self.size=(len(self.grid),len(self.grid[0]))
        self.assign_neighbor()
        
    def export(self, url):
        """
        Fonction qui exporte notre labyrinthe au format csv.

        Input :
            url : string, url du fichier csv à créer
        """
        with open(url, 'w', encoding='utf-8') as file:
            csvWriter=csv.writer(file,delimiter=';')
            for i in self.grid:
                to_write=[str(j) for j in i]
                csvWriter.writerow(to_write)
        
    def assign_neighbor(self):
        """
        Fonction qui crée les liste de voisinage de toutes les cases du labyrinthe.
        """
        for line in self.grid:
            for node in line:
                node.set_labyrinthe(self)
                for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if 0<=(node.coordinates[1]+dx)<self.size[0] and 0<=(node.coordinates[0]+dy)<self.size[1]:
                        node.set_neighbor(self.grid[node.coordinates[1]+dx][node.coordinates[0]+dy])



    def solving_A_star(self):
        """
        Fonction qui cherche le plus court chemin entre le point de départ et le point d'arrivée en utilisant l'algorithme A*.
        """
        a_decouvrir = PriorityQueue()
        a_decouvrir.put((0,self.start))
        while a_decouvrir.empty() == False :
            self.sequence_affichage['A*'].append([])
            score_actuel,actuel = a_decouvrir.get()
            actuel.solving_state= "explored"
            if actuel!=self.start and actuel!=self.end:
                self.sequence_affichage['A*'][-1].append((actuel.animation_pixel_id,'explored'))
            if actuel == self.end :
                chemin_suivi = self.get_final_path()
                for i in chemin_suivi[1:-1]:
                    self.sequence_affichage['A*'][-1].append((i.animation_pixel_id,'solution'))
                while a_decouvrir.empty() == False :
                    a_decouvrir.get()
            else :
                for voisin in actuel.neighbor :
                    if voisin.parent == None and voisin.type in ["path","end"] :
                        score_voisin = voisin.get_A_score(self.end)
                        a_decouvrir.put((score_voisin,voisin))
                        voisin.solving_state = "identified"
                        if voisin!=self.start and voisin!=self.end:
                            self.sequence_affichage['A*'][-1].append((voisin.animation_pixel_id,'identified'))
                        voisin.parent = actuel
        cell_to_clear=[]
        for sequence in self.sequence_affichage['A*']:
            for cell_pixel_id,newstate in sequence :
                if cell_pixel_id not in cell_to_clear:
                    cell_to_clear.append(cell_pixel_id)
        self.sequence_affichage['A*'].append([(cell_pixel_id,'path') for cell_pixel_id in cell_to_clear])
        self.clear_solving_state()
    
    def solving_BFS(self):
        """
        Fonction qui cherche le plus court chemin entre le point de départ et le point d'arrivée en utilisant l'algorithme BFS.
        """
        to_explore=[self.start]
        actuel=None
        while actuel !=self.end and len(to_explore):
            self.sequence_affichage['BFS'].append([])
            actuel=to_explore.pop(0)
            actuel.solving_state='explored'
            if actuel!=self.start and actuel!=self.end:
                self.sequence_affichage['BFS'][-1].append((actuel.animation_pixel_id,'explored'))
            for voisin in actuel.neighbor:
                if voisin.parent == None and voisin.type in ["path","end"] :
                    to_explore.append(voisin)
                    voisin.solving_state='identified'
                    if voisin!=self.start and voisin!=self.end:
                            self.sequence_affichage['BFS'][-1].append((voisin.animation_pixel_id,'identified'))
                    voisin.parent=actuel
        chemin_suivi = self.get_final_path()
        for i in chemin_suivi[1:-1]:
            self.sequence_affichage['BFS'][-1].append((i.animation_pixel_id,'solution'))
        cell_to_clear=[]
        for sequence in self.sequence_affichage['BFS']:
            for cell_pixel_id,newstate in sequence :
                if cell_pixel_id not in cell_to_clear:
                    cell_to_clear.append(cell_pixel_id)
        self.sequence_affichage['BFS'].append([(cell_pixel_id,'path') for cell_pixel_id in cell_to_clear])
        self.clear_solving_state()
    
    def solving_DFS(self):
        """
        Fonction qui cherche le plus court chemin entre le point de départ et le point d'arrivée en utilisant l'algorithme DFS.
        """
        to_explore=[self.start]
        actuel=None
        while actuel !=self.end and len(to_explore):
            self.sequence_affichage['DFS'].append([])
            actuel=to_explore.pop(0)
            actuel.solving_state='explored'
            if actuel!=self.start and actuel!=self.end:
                self.sequence_affichage['DFS'][-1].append((actuel.animation_pixel_id,'explored'))
            for voisin in actuel.neighbor:
                if voisin.parent == None and voisin.type in ["path","end"] :
                    to_explore.insert(0,voisin)
                    voisin.solving_state='identified'
                    if voisin!=self.start and voisin!=self.end:
                            self.sequence_affichage['DFS'][-1].append((voisin.animation_pixel_id,'identified'))
                    voisin.parent=actuel
        chemin_suivi = self.get_final_path()
        for i in chemin_suivi[1:-1]:
            self.sequence_affichage['DFS'][-1].append((i.animation_pixel_id,'solution'))
        cell_to_clear=[]
        for sequence in self.sequence_affichage['DFS']:
            for cell_pixel_id,newstate in sequence :
                if cell_pixel_id not in cell_to_clear:
                    cell_to_clear.append(cell_pixel_id)
        self.sequence_affichage['DFS'].append([(cell_pixel_id,'path') for cell_pixel_id in cell_to_clear])
        self.clear_solving_state()

    def clear_solving_state(self):
        """
        Fonction qui supprime les données nécessaires à la résolution du dernier algorithme utilisé.
        """
        for i in self.grid:
            for cell in i:
                cell.solving_state='unexplored'
                cell.parent=None

    
    def get_final_path(self):
        """
        Fonction qui retrace le chemin suivi depuis l'arrivée vers le départ.

        Output :
            chemin : liste, chemin le plus court entre les 2 points
        """
        if self.end.parent is not None:
            chemin = [self.end]
            while chemin[0] != self.start :
                chemin.insert(0,chemin[0].parent)
            return chemin
        return []

    def get_case_from_id(self,id):
        """
        Fonction qui permet de récupérer un objet case à partir de son attribut "pixel_id".

        Input :
            id : string, id du pixel sur le canvas 

        Output :
            case : Case, objet case qui correspond au "pixel_id"
        """
        i = 0
        j = 0
        case = None
        find = False
        while find == False and i <= self.size[0]-1:
            while find == False and j <= self.size[1]-1:
                if self.grid[i][j].pixel_id == int(id) :
                    case = self.grid[i][j]
                    find = True
                j+=1
            i+=1
            j=0
        return case

class Case:
    """
    Cette classe sert à paramétrer les cases de notre labyrinthe.  
    """
    def __init__(self,csv_data):
        """csv data : [(x,y),type]
            type : wall, path, start, end"""
        self.coordinates=(int(csv_data[0][0]),int(csv_data[0][1]))
        self.type=csv_data[1]
        self.neighbor=[]
        self.solving_state='unexplored'
        self.pixel_id=None
        self.animation_pixel_id=None
        self.parent=None

    def set_neighbor(self,other):
        """
        Fonction qui permet de définir les cases voisines d'une case.

        Input :
            other : Case, id de la case qui est voisine de notre case
        """
        self.neighbor.append(other)

    def set_labyrinthe(self,labyrinthe):
        """
        Fonction qui permet de définir les cases de départ et d'arrivée du labyrinthe ainsi que de définir le labyrinthe auquel appartient la case.

        Input :
            labyrinthe : Labyrinthe, id du labyrinthe sur lequel se trouve la case
        """
        self.labyrinthe=labyrinthe
        if self.type=='end':
            labyrinthe.end=self
        elif self.type=='start':
            labyrinthe.start=self
    
    def get_A_score(self,arrivee) :
        """
        Fonction qui calcule le score d'un point du labyrinthe en fonction de sa distance au point d'arrivée.

        Input :
            point : case, point où l'on souhaite calculer le score
            arrivee : case, point d'arrivée du labyrinthe

        Output :
            score : float, score du point
        """
        score = sqrt((self.coordinates[0]-arrivee.coordinates[0])**2+(self.coordinates[1]-arrivee.coordinates[1])**2)
        return score

    def __str__(self):
        return f'[{self.coordinates},"{self.type}"]'

    def __repr__(self):
        return str(self)
    
    def __eq__(self,other):
        return id(self)==id(other)

    def __lt__(self,other):
        return id(self)<id(other)

