import tkinter as tk
import Grille

class Cube:

	couleur_haut = "#afafaf"
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
	def __init__(self,pcanvas,pgrille,pcoordsGrille,phauteur=0,pcouleur=(couleur_haut,couleur_gauche,couleur_droite)):
		# pcoords est un point de la grille, (hauteur 0 !!)

		self.coords = pgrille.grilleToCanvas(pcoordsGrille)

		self.dessiner(pcanvas,pgrille,phauteur,pcouleur)

		self.__id = self.__haut

	# destructeur
	def __del__(self):
		# print("destruction d'un cube")
		return

	def dessiner(self,pcanvas,pgrille,phauteur,pcouleur):
		d = pgrille.definition
		
		x = self.coords[0]
		y = self.coords[1]
		self.__h = phauteur


		A = (x-d,y-d/2) # haut gauche
		B = (x+d,y-d/2) # haut droite
		C = (x-d,y+d/2) # bas gauche
		D = (x+d,y+d/2) # bas droite
		E = (x,y+d) # bas
		F = (x,y-d) # haut
		
		# on ajoute un tag aux faces, pour que quand on clique sur une face, on puisse avoir le cube
		self.__haut = pcanvas.create_polygon(self.coords,B,F,A,fill=pcouleur[0],outline="black")
		tag = "cube_"+str(self.__haut)
		pcanvas.itemconfig(self.__haut,tags=tag)
		
		self.__gauche = pcanvas.create_polygon(self.coords,A,C,E,fill=pcouleur[1],outline="black",tags=tag)
		self.__droite = pcanvas.create_polygon(self.coords,B,D,E,fill=pcouleur[2],outline="black",tags=tag)

	def effacer(self,pcanvas):
		pcanvas.delete(self.__haut,self.__gauche,self.__droite)
