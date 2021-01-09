import tkinter as tk
import grille

class Cube:

    __couleur_haut = "#afafaf"
    __couleur_gauche = "#808080"
    __couleur_droite = "#414141"

    @property
    def couleur(self):
        return (
            self.__couleur_haut,
            self.__couleur_gauche,
            self.__couleur_droite)

    @property
    def haut(self):
        return self.__haut

    @property
    def gauche(self):
        return self.__gauche

    @property
    def droite(self):
        return self.__droite

    @property
    def id(self):
        return self.__id

    @property
    def numero(self):
        return self.__numero

    @property
    def h(self):
        return self.__h
    @h.setter
    def h(self,ph):
        self.__h = ph

    @property
    def coords(self):
        return self.__coords
    @coords.setter
    def coords(self,pcoordsCanvas):
        self.__coords = pcoordsCanvas
    

    # Constructeur
    def __init__(self,pcanvas,pgrille,
                 pcoords_grille,phauteur=0,
                 pcouleur=(__couleur_haut,__couleur_gauche,__couleur_droite),
                 pnumero=0):
        # note : pcoords_grille est un point de la grille (hauteur 0)

        self.__canvas = pcanvas
        self.__grille = pgrille
        self.__coords = pgrille.grille_to_canvas(pcoords_grille)
        self.__h = phauteur
        self.__numero = pnumero

        self.dessiner(pcouleur)

        self.__id = self.__haut

    def dessiner(self,pcouleur):
        d = self.__grille.definition
        
        x = self.__coords[0]
        y = self.__coords[1]

        A = (x-d,y-d/2) # haut gauche
        B = (x+d,y-d/2) # haut droite
        C = (x-d,y+d/2) # bas gauche
        D = (x+d,y+d/2) # bas droite
        E = (x,y+d) # bas
        F = (x,y-d) # haut
        
        # on ajoute un tag aux faces pour toutes les avoir avec 1 seule
        self.__haut = self.__canvas.create_polygon(
            self.__coords, B,F,A, outline="black")
        tag = "cube_"+str(self.__haut) # tag de la forme "cube_idfaceduhaut"
        self.__canvas.itemconfig(self.__haut,tags=tag)
        
        self.__gauche = self.__canvas.create_polygon(
            self.__coords, A,C,E,
            outline="black",tags=tag)
        self.__droite = self.__canvas.create_polygon(
            self.__coords, B,D,E,
            outline="black",tags=tag)

        self.changer_couleur(pcouleur)

    def selection_cube(self):
        self.changer_couleur('red')

    def deselection_cube(self):
        self.changer_couleur((
            self.__couleur_haut,
            self.__couleur_gauche,
            self.__couleur_droite))

    def effacer(self):
        self.__canvas.delete(self.__haut,self.__gauche,self.__droite)

    def changer_couleur(self,pcouleur):
        """
        pcouleur est soit une str comme 'red'
        soit un tuple de 3 chaines en hexadecimal commençant par #
        """
        if type(pcouleur) == str:
            self.__canvas.itemconfig("cube_"+str(self.__haut),fill=pcouleur)
        else:
            self.__couleur_haut = pcouleur[0]
            self.__couleur_gauche = pcouleur[1]
            self.__couleur_droite = pcouleur[2]
            self.__canvas.itemconfig(self.__haut,fill=pcouleur[0])
            self.__canvas.itemconfig(self.__gauche,fill=pcouleur[1])
            self.__canvas.itemconfig(self.__droite,fill=pcouleur[2])

    def desactiver(self):
        """
        'Desactive' le cube, le rendant insensible
        aux bindings (pour la previsualisation)
        """
        self.__canvas.itemconfig("cube_"+str(self.__haut),state='disabled')

    def priorite(self):
        """Rend le cube visible au premier plan, devant tous les autres"""
        self.__canvas.tag_raise("cube_"+str(self.__haut))

    def coords_to_3D(self):
        """
        Retourne les coordonnees de la case "de base" sur lequel le cube est.
        Note : va au point le plus proche, car on aurait des float sinon.
        Note 2 : c'est une fonction car les coordonnees changent.
        """
        coordsGrille = self.__grille.closest_point(
            self.__grille.canvas_to_grille(self.__coords))
        return (coordsGrille[0]+self.__h, coordsGrille[1]+self.__h)
