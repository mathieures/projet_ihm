import tkinter as tk
import Grille
import Cube

class App:

	def addCubeToDico(self,pcoordsGrille,phauteur):
		x,y = pcoordsGrille
		if((x,y) in self.DICO):
			self.DICO[(x,y)].append(phauteur)
		else:
			self.DICO[(x,y)] = phauteur
		print("new dico :",self.DICO)

	def nouveauFichier(self):
		# on efface tous les cubes
		for cube in self.CUBES:
			cube.effacer(self.canv)
		# self.canv.delete("tag_cube") # plus simple a ecrire qu'appeler Cube.effacer() pour tous les cubes
		self.CUBES = []
		self.DICO = {}
		# on desactive l'option de sauvegarde
		# self.deroulFichier.entryconfigure(2,state="disabled")

	def annulerDernierCube(self,event):
		"""Annule le dernier placement de cube."""
		if len(self.CUBES) == 1:
			# on desactive l'option pour annuler
			self.deroulFichier.entryconfigure(1,state="disabled")
		if len(self.CUBES) > 0:
			cube = self.CUBES[-1]
			self.CUBES[-1].effacer(self.canv)
			self.CUBES.pop()
			del self.DICO[self.grille.canvasToGrille(cube.coords)]
		else:
			print("plus de cubes dans la liste")

	def placerCube(self,pcoordsGrille,phauteur):
		"""Prend en parametre des coordonnes de self.grille (peut-etre a changer ?)"""
		coords = self.grille.closestPointUp(pcoordsGrille)
		print("		placed cube at :",coords)
		cube = Cube.Cube(self.canv,self.grille,coords,ptags="tag_cube")
		self.addCubeToDico(coords,phauteur)
		# on a la hauteur en cliquant sur une face du haut
		# il faut passer les coordonnees du cube mais avec la hauteur +1
		self.CUBES.append(cube)
		self.deroulFichier.entryconfigure(1,state="active")
		return cube # sert a rien mais au cas ou


	def onClick(self,event):
		currentCoords = (event.x,event.y)
		convertedCoords = self.grille.canvasToGrille((currentCoords))
		print("click on :",currentCoords,"=>",convertedCoords)
		hauteur = 5 # a changer avec la hauteur du cube sur lequel on a clique
		if convertedCoords[0] < self.grille.taille_x and convertedCoords[1] < self.grille.taille_y and convertedCoords[0] > 0 and convertedCoords[1] > 0:
			self.placerCube(convertedCoords,hauteur)

	def onMotion(self,event):
		currentCoords = (event.x,event.y)
		convertedCoords = self.grille.canvasToGrille((currentCoords))
		print("click on :",currentCoords,"=>",convertedCoords)
		self.placerCube(convertedCoords)

	def __init__(self):

		self.CUBES = [] # liste des cubes places


		# Root
		self.root = tk.Tk()

		# Menus

		self.menuFrame = tk.Frame(self.root,bg="red")
		self.menuFrame.pack(side=tk.TOP,expand=True,fill=tk.X,anchor="n")

		self.bottomFrame = tk.Frame(self.root,bg="blue")
		self.bottomFrame.pack(side=tk.BOTTOM,expand=True,fill=tk.X,anchor="s")

		# Menu fichier
		self.menuFichier = tk.Menubutton(self.menuFrame,text="Fichier",underline=0,relief="raised")

		self.deroulFichier = tk.Menu(self.menuFichier, tearoff=False)
		self.deroulFichier.add_command(label="Nouveau", command=self.nouveauFichier)
		self.deroulFichier.add_command(label="Annuler", command=self.annulerDernierCube)
		self.root.bind("<Control-z>", lambda event:self.annulerDernierCube(event))

		# on desactive l'option pour annuler
		self.deroulFichier.entryconfigure(1,state="disabled")

		# self.deroulFichier.add_command(label="Ouvrir", command=openFile)
		# self.deroulFichier.add_command(labstateel="Sauver", command=saveFile)
		# self.deroulFichier.add_command(label="Quitter", command=quitApp)
		# self.root.protocol("WM_DELETE_WINDOW", quitApp) # pour gerer la fermeture avec la croix rouge et alt-f4

		# # on desactive l'option de sauvegarde (il faudrait trouver par nom plutot)
		# self.deroulFichier.entryconfigure(2,state="disabled")

		self.menuFichier.config(menu=self.deroulFichier)
		self.menuFichier.pack(side=tk.LEFT)

		# Menu aide

		self.menuAide = tk.Menubutton(self.menuFrame,text="Aide",underline=0,relief="raised")

		self.derouleAide = tk.Menu(self.menuAide,tearoff=False)

		self.menuAide.config(menu=self.derouleAide)
		self.menuAide.pack(side=tk.RIGHT)

		# Canvas

		self.canv = tk.Canvas(self.root,width=500,height=500,bg="white")
		self.canv.bind("<Button-1>",self.onClick)

		self.grille = Grille.Grille(self.canv)

		# cube1 = Cube.Cube(self.canv,self.grille,(1,1))

		# DICO
		self.DICO = {}

		self.canv.pack()
		# print("is ready :",isReadyToDraw)


		# Fin

		self.root.mainloop()


App()

exit(0)
