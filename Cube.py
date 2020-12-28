import tkinter as tk
import Grille

class Cube:

	__couleur_haut = "#afafaf"
	__couleur_gauche = "#808080"
	__couleur_droite = "#414141"

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

	@property
	def couleur(self):
		return (self.__couleur_haut, self.__couleur_gauche, self.__couleur_droite)

	#constructeur
	def __init__(self,pcanvas,pgrille,pcoordsGrille,phauteur=0,pcouleur=(__couleur_haut,__couleur_gauche,__couleur_droite)):
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
		self.__haut = pcanvas.create_polygon(self.coords,B,F,A,outline="black")
		tag = "cube_"+str(self.__haut)
		pcanvas.itemconfig(self.__haut,tags=tag)
		
		self.__gauche = pcanvas.create_polygon(self.coords,A,C,E,outline="black",tags=tag)
		self.__droite = pcanvas.create_polygon(self.coords,B,D,E,outline="black",tags=tag)

		self.changerCouleur(pcanvas,pcouleur)

	def selectionCube(self,pcanvas):
		pcanvas.itemconfig("cube_"+str(self.__haut),fill='red')

	def deselectionCube(self,pcanvas):
		pcanvas.itemconfig(self.__haut,fill=self.couleur[0])
		pcanvas.itemconfig(self.__gauche,fill=self.couleur[1])
		pcanvas.itemconfig(self.__droite,fill=self.couleur[2])

	def effacer(self,pcanvas):
		pcanvas.delete(self.__haut,self.__gauche,self.__droite)

	def changerCouleur(self,pcanvas,pcouleur):
		"""
		pcouleur est un tuple/liste de 3 chaines en hexadecimal commençant par #
		"""
		pcanvas.itemconfig(self.__haut,fill=pcouleur[0])
		pcanvas.itemconfig(self.__gauche,fill=pcouleur[1])
		pcanvas.itemconfig(self.__droite,fill=pcouleur[2])
		self.__couleur_haut = pcouleur[0]
		self.__couleur_gauche = pcouleur[1]
		self.__couleur_droite = pcouleur[2]

	def desactiver(self,pcanvas):
		# fonction qui "desactive" le cube, il sera insensible aux bindings (pour la previsualisation)
		pcanvas.itemconfig("cube_"+str(self.__haut),state='disabled')

	def priorite(self,pcanvas):
		# fonction pour rendre le cube visible au premier plan
		pcanvas.tag_raise("cube_"+str(self.__haut))
