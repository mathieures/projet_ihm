import tkinter as tk
import Grille

class Cube:
	couleur_haut = "#bfbfbf"
	couleur_gauche = "#808080"
	couleur_droite = "#414141"

	def __init__(self,pcanvas,pgrille,pcoordsGrille):
		# pcoords est un point de la grille
		d = pgrille.definition
		centre = pgrille.grilleToCanvas(pcoordsGrille) 
		
		# dessin
		x = centre[0]
		y = centre[1]
		
		A = (x-d,y-d/2) # haut gauche
		B = (x+d,y-d/2) # haut droite
		C = (x-d,y+d/2) # bas gauche
		D = (x+d,y+d/2) # bas droite
		E = (x,y+d) # bas
		F = (x,y-d) # haut
		haut = pcanvas.create_polygon(centre,B,F,A,fill='#afafaf')
		gauche = pcanvas.create_polygon(centre,A, C, E,fill='#414141')
		droite = pcanvas.create_polygon(centre,B,D, E,fill='#808080')
		# self.dessine(pcanvas, d, centre)


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