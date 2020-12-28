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

	def _get_h(self):
		return self.__h
	def _set_h(self,ph):
		self.__h = ph
	h = property(_get_h, _set_h)

	def _get_couleur(self):
		return (self.__couleur_haut, self.__couleur_gauche, self.__couleur_droite)
	couleur = property(_get_couleur)

	def _set_coords(self,pcoordsCanvas):
		self.__coords = pcoordsCanvas
	def _get_coords(self):
		return self.__coords
	coords = property(_get_coords, _set_coords)
	

	#constructeur
	def __init__(self,pcanvas,pgrille,pcoordsGrille,phauteur=0,pcouleur=(__couleur_haut,__couleur_gauche,__couleur_droite)):
		# pcoordsGrille est un point de la grille, (hauteur 0 !!)

		self.__canvas = pcanvas
		self.__grille = pgrille
		self.__coords = pgrille.grilleToCanvas(pcoordsGrille)
		self.__h = phauteur

		self.dessiner(pcouleur)

		self.__id = self.__haut

	# destructeur
	def __del__(self):
		# print("destruction d'un cube")
		return

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
		
		# on ajoute un tag aux faces, pour que quand on clique sur une face, on puisse avoir le cube
		self.__haut = self.__canvas.create_polygon(self.__coords,B,F,A,outline="black")
		tag = "cube_"+str(self.__haut)
		self.__canvas.itemconfig(self.__haut,tags=tag)
		
		self.__gauche = self.__canvas.create_polygon(self.__coords,A,C,E,outline="black",tags=tag)
		self.__droite = self.__canvas.create_polygon(self.__coords,B,D,E,outline="black",tags=tag)

		self.changerCouleur(pcouleur)

	def selectionCube(self):
		self.changerCouleur('red')

	def deselectionCube(self):
		self.changerCouleur((self.__couleur_haut,self.__couleur_gauche,self.__couleur_droite))

	def effacer(self):
		self.__canvas.delete(self.__haut,self.__gauche,self.__droite)

	def changerCouleur(self,pcouleur):
		"""
		pcouleur est soit une str comme 'red' soit un tuple de 3 chaines en hexadecimal commençant par #
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
		# fonction qui "desactive" le cube, il sera insensible aux bindings (pour la previsualisation)
		self.__canvas.itemconfig("cube_"+str(self.__haut),state='disabled')

	def priorite(self):
		# fonction pour rendre le cube visible au premier plan
		self.__canvas.tag_raise("cube_"+str(self.__haut))

	def coordsTo3D(self):
		"""
		Retourne les coordonnees de la case "de base" sur lequel le cube est.
		Note : ne va pas au point le plus proche, car on pourrait vouloir transformer des coordonnees precises.
		"""
		coordsGrille = self.__grille.canvasToGrille(self.__coords)
		return (coordsGrille[0]+self.__h, coordsGrille[1]+self.__h)
