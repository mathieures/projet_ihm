import tkinter as tk

class Grille:
    @property
    def definition(self):
        return self.__definition

    @property
    def taille_x(self):
        return self.__taille_x

    @property
    def taille_y(self):
        return self.__taille_y

    @property
    def origine(self):
        return self.__origine

    def __init__(self, pcanvas, pdefinition=20,
                 ptaille_x=10, ptaille_y=10, porigine=None):
        """
        L'origine est passee en parametre si on veut la placer a un endroit
        particulier (comme pour la fenetre de selection de couleur)
        """
        self.__definition = pdefinition # taille des cotés d'un carre
        # nombre de cases sur l'axe x (qui va en bas à droite)
        #  et l'axe y (qui va en bas à gauche)
        self.__taille_x = ptaille_x
        self.__taille_y = ptaille_y 

        # coordonnees de l'origine (dans le referentiel tkinter)
        if porigine is None:
            self.__origine = (int(pcanvas.cget("width")) / 2,
                              int(pcanvas.cget("height")) / 3)
        else:
            self.__origine = porigine
            
        print("origine :", self.__origine,"; definition :", self.definition)
        # dessin de la grille
        self.dessine_grille(pcanvas)

    def dessine_grille(self, pcanvas):
        """Dessine la grille"""
        x = self.__origine[0]
        y = self.__origine[1]
        d = self.definition
        for i in range(self.taille_y+1):
            pcanvas.create_line(x, y, x+d*self.taille_x, y+(d*self.taille_x/2))
            x -= d
            y += d/2
        x = self.__origine[0]
        y = self.__origine[1]
        for j in range(self.taille_x+1):
            pcanvas.create_line(x, y, x-d*self.taille_y, y+(d*self.taille_y/2))
            x += d
            y += d/2

    def grille_to_canvas(self, pcoords):
        """
        Convertit des coordonnees du referentiel tkinter
        vers des coordonnees de la Grille (2D)
        """
        orig = self.__origine
        d = self.__definition
        x = (orig[0] + pcoords[0] * d) - (pcoords[1] * d)
        y = (orig[1] + pcoords[0] * (d/2)) + (pcoords[1] * (d/2))
        return (x, y)

    def canvas_to_grille(self, pcoords):
        """
        Convertit des coordonnees de la Grille (2D)
        vers des coordonnees du referentiel tkinter
        """
        orig = self.__origine
        d = self.__definition
        i = (pcoords[1] - orig[1])/d + (pcoords[0] - orig[0])/(2*d)
        j = (pcoords[1] - orig[1])/d - (pcoords[0] - orig[0])/(2*d)
        return (i, j)

    def closest_point(self, pcoords_grille):
        """
        Prend en parametre des coordonnees de grille, retourne le point
        de la grille (une intersection de lignes) le plus proche.
        Note : si on veut prendre en parametre des coordonnees
        de canvas, on peut les convertir avant.
        """
        x, y = pcoords_grille
        if x > int(x) + 0.5:
            x = int(x) + 1 # on arrondit au superieur
        else:
            x = int(x)
        if y > int(y) + 0.5:
            y = int(y) + 1 # on arrondit au superieur
        else:
            y = int(y)
        return (x, y)

    def closest_point_up(self, pcoords_grille):
        """Meme chose que closest_point() mais 0.5 case plus haut"""
        return self.closest_point(
            (pcoords_grille[0]-0.5,
             pcoords_grille[1]-0.5))

    def is_in_grille(self, pcoords):
        coords_grille = self.canvas_to_grille(pcoords)
        if (coords_grille[0] < self.taille_x and
            coords_grille[1] < self.taille_y and
            coords_grille[0] > 0 and
            coords_grille[1] > 0):
            return True
        return False
