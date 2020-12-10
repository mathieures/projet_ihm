import tkinter as tk
import Grille

class Cube:

	couleur_haut = "#bfbfbf"
	couleur_gauche = "#808080"
	couleur_droite = "#414141"

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
	def h(self):
		return self.__h

	#constructeur
	def __init__(self,pcanvas,pgrille,pcoordsGrille,phauteur=0):
		# pcoords est un point de la grille, (hauteur 0 !!)
		d = pgrille.definition

		self.coords = pgrille.grilleToCanvas(pcoordsGrille)

		# dessin
		x = self.coords[0]
		y = self.coords[1]
		self.__h = phauteur
		print("hauteur :",self.__h)


		A = (x-d,y-d/2) # haut gauche
		B = (x+d,y-d/2) # haut droite
		C = (x-d,y+d/2) # bas gauche
		D = (x+d,y+d/2) # bas droite
		E = (x,y+d) # bas
		F = (x,y-d) # haut
		
		# on ajoute un tag aux faces, pour que quand on clique sur une face, on puisse avoir le cube
		self.__haut = pcanvas.create_polygon(self.coords,B,F,A,fill='#afafaf',outline="black")
		tag = "cube_"+str(self.__haut)
		pcanvas.itemconfig(self.__haut,tags=tag)
		
		self.__gauche = pcanvas.create_polygon(self.coords,A,C,E,fill='#414141',outline="black",tags=tag)
		self.__droite = pcanvas.create_polygon(self.coords,B,D,E,fill='#808080',outline="black",tags=tag)

		# self.dessine(pcanvas, d, self.coords)

		self.__id = self.__haut

	# destructeur
	def __del__(self):
		print("destruction d'un cube")

	def effacer(self,pcanvas):
		pcanvas.delete(self.__haut,self.__gauche,self.__droite)
