import tkinter as tk
import Grille

class Cube:

	couleur_haut = "#bfbfbf"
	couleur_gauche = "#808080"
	couleur_droite = "#414141"

	#constructeur
	def __init__(self,pcanvas,pgrille,pcoordsGrille,ptags=None,phauteur=0):
		# pcoords est un point de la grille
		d = pgrille.definition
		self.coords = pgrille.grilleToCanvas(pcoordsGrille)

		# dessin
		x = self.coords[0]
		y = self.coords[1]
		self.h = phauteur


		A = (x-d,y-d/2) # haut gauche
		B = (x+d,y-d/2) # haut droite
		C = (x-d,y+d/2) # bas gauche
		D = (x+d,y+d/2) # bas droite
		E = (x,y+d) # bas
		F = (x,y-d) # haut
		self.__haut = pcanvas.create_polygon(self.coords,B,F,A,fill='#afafaf',outline="black",tags=ptags)
		self.__gauche = pcanvas.create_polygon(self.coords,A, C, E,fill='#414141',outline="black",tags=ptags)
		self.__droite = pcanvas.create_polygon(self.coords,B,D, E,fill='#808080',outline="black",tags=ptags)
		# self.dessine(pcanvas, d, self.coords)

		self.id = self.__haut

	# destructeur
	def __del__(self):
		print("destruction d'un cube")

	def effacer(self,pcanvas):
		pcanvas.delete(self.__haut,self.__gauche,self.__droite)

	# def dessine(self,pcanvas,d,pcoords):
	# 	AB = [x-d,y-d/2]
	# 	EB = [x+d,y-d/2]
	# 	AC = [x-d,y+d/2]
	# 	EC = [x+d,y+d/2]
	# 	xD = [x,y+d]
	# 	xF = [x,y-d]
	# 	haut = pcanvas.create_polygon(x,y,EB,xF,AB,fill='#afafaf')
	# 	gauche = pcanvas.create_polygon(x,y,AB, AC, xD,fill='#414141')
	# 	droite = pcanvas.create_polygon(x,y,EB,EC, xD,fill='#808080')
