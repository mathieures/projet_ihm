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

	def __init__(self,pcanvas,pdefinition=20,ptaille_x=10,ptaille_y=10,porigine=None):
		self.__definition = pdefinition # taille des cotes d'un carre
		self.__taille_x = ptaille_x # nombre de cases suivant l'axe x (qui va en bas à droite)
		self.__taille_y = ptaille_y # nombre de cases suivant l'axe y (qui va en bas à gauche)

		if porigine == None:
			self.__origine = (int(pcanvas.cget("width")) / 2,int(pcanvas.cget("height")) / 4) # coordonnees de l'origine (dans le referentiel tkinter)
		else:
			self.__origine = porigine
			
		print("origine :",self.__origine,"; definition :",self.definition)
		# dessin de la grille
		self.dessineGrille(pcanvas)

	def dessineGrille(self,pcanvas):
		x = self.__origine[0]
		y = self.__origine[1]
		d = self.definition
		for i in range(self.taille_y+1):
			pcanvas.create_line(x,y,x+d*self.taille_x,y+(d*self.taille_x/2))
			x -= d
			y += d/2
		x = self.__origine[0]
		y = self.__origine[1]
		for j in range(self.taille_x+1):
			pcanvas.create_line(x,y,x-d*self.taille_y,y+(d*self.taille_y/2))
			x += d
			y += d/2

	def grilleToCanvas(self,pcoords):
		"""
		Convertit des coordonnees du referentiel tkinter
		vers des coordonnees de la Grille (2D)
		"""
		orig = self.__origine
		d = self.__definition
		x = orig[0] + pcoords[0] * d - pcoords[1] * d
		y = orig[1] + (pcoords[0]) * (d/2) + (pcoords[1]) * (d/2)
		return (x, y)

	def canvasToGrille(self,pcoords):
		"""
		Convertit des coordonnees de la Grille (2D)
		vers des coordonnees du referentiel tkinter
		"""
		orig = self.__origine
		d = self.__definition
		i = (pcoords[1] - orig[1])/d + (pcoords[0] - orig[0])/(2*d)
		j = (pcoords[1] - orig[1])/d - (pcoords[0] - orig[0])/(2*d)
		return (i, j)

	def closestPoint(self,pcoordsGrille):
		"""
		Prend en parametre des coordonnees de grille
		et retourne le point (intersection) la plus proche
		(a noter que si on veut prendre en parametre des coords de canvas,
		on peut juste les convertir avant)
		"""
		x, y = pcoordsGrille
		if(x > int(x) + 0.5):
			x = int(x) + 1 # on arrondit au superieur
		else:
			x = int(x)
		if(y > int(y) + 0.5):
			y = int(y) + 1 # on arrondit au superieur
		else:
			y = int(y)
		return (x,y)

	def closestPointUp(self,pcoordsGrille):
		return self.closestPoint((pcoordsGrille[0]-0.5,pcoordsGrille[1]-0.5))

	def is_in_grille(self,pcoords):
		coordsGrille = self.canvasToGrille(pcoords)
		if(coordsGrille[0] < self.taille_x and coordsGrille[1] < self.taille_y and
				coordsGrille[0] > 0 and coordsGrille[1] > 0):
			return True
		return False
