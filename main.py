import tkinter as tk
import Grille
import Cube
from tkinter import filedialog,messagebox

class App:

	def addCubeToDico(self,pcoordsGrille,phauteur):
		x,y = pcoordsGrille
		if((x,y) in self.DICO):
			self.DICO[(x,y)].append(phauteur)
		else:
			self.DICO[(x,y)] = [phauteur]
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

	def sauverFichier(self):
		fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", ".txt"),("All files", ".*"))) # On demande a l'utilisateur dans quel fichier il veut sauver le projet
		try: # On ecrit dans le fichier les valeurs du dico
			with open(fichier, "w", encoding = "utf-8") as f:
				for pos_cube in self.DICO:
					f.write(str(pos_cube[0]) + "," + str(pos_cube[1]) + " ")
					for h in self.DICO[pos_cube]:
						f.write(str(h) + " ")
					f.write("\n")
		except: # Si il y a une erreur, le dire a l'utilisateur, (gerer les differentes erreurs apres !!!!)
			messagebox.showerror(title="Error", message="Erreur lors de l'ouverture du fichier.")
			# attention : appele aussi quand l'utilisateur clique sur Annuler

	def ouvrirFichier(self):
		self.nouveauFichier()
		fichier = filedialog.askopenfile(mode="r",defaultextension=".txt", filetypes=(("Text files", ".txt"),("All files", ".*")))
		if(fichier):
			positions = fichier.readlines()
			for pos_cube in positions:
				parse = pos_cube.rstrip().split(" ")
				pos = parse[0].split(",") # On prend le permier element de parse qui sera la position du cube, les autres elements sont les hauteurs
				for i in range(1,len(parse)):
					self.placerCube((int(pos[0]),int(pos[1])),int(parse[i])) 
			fichier.close()

	def annulerDernierCube(self,event=None):
		"""Annule le dernier placement de cube."""
		# le parametre event est obligatoire pour etre bind
		if len(self.CUBES) == 1:
			# on desactive l'option pour annuler
			self.deroulFichier.entryconfigure(2,state="disabled")
		if len(self.CUBES) > 0:
			cube = self.CUBES[-1]
			coordsGrille = self.grille.canvasToGrille(cube.coords)
			self.DICO[(coordsGrille[0]+cube.h,coordsGrille[1]+cube.h)].pop()
			self.CUBES[-1].effacer(self.canv)
			self.CUBES.pop()
		else:
			print("plus de cubes dans la liste")


	def placerCube(self,pcoordsGrille,phauteur):
		"""Prend en parametre des coordonnes de self.grille (peut-etre a changer ?)"""

		coords = self.grille.closestPoint(pcoordsGrille)
		print("coords 3D :",coords,phauteur,end=" ; ")
		self.addCubeToDico(coords,phauteur) # coordonnees 3D

		# on transforme les coordonnees 3D en coordonnees 2D
		coords = (coords[0]-phauteur,coords[1]-phauteur)
		print("coords 2D :",coords)


		print("  placed cube at :",coords)
		cube = Cube.Cube(self.canv,self.grille,coords,phauteur)
		# on a la hauteur en cliquant sur une face du haut
		# il faut passer les coordonnees du cube mais avec la hauteur +1
		self.CUBES.append(cube)
		self.deroulFichier.entryconfigure(2,state="active")
		self.deroulFichier.entryconfigure(3,state="active")
		return cube # sert a rien mais au cas ou

	def placerCubeHaut(self,pposition3D):
		x,y,h = pposition3D
		self.placerCube((x,y),h+1)

	def placerCubeGauche(self,pposition3D):
		x,y,h = pposition3D
		self.placerCube((x,y+1),h)

	def placerCubeDroite(self,pposition3D):
		x,y,h = pposition3D
		self.placerCube((x+1,y),h)


	def onClick(self,event):
		currentCoords = (event.x,event.y)
		convertedCoords = self.grille.canvasToGrille((currentCoords))
		print("click on :",currentCoords,"=>",convertedCoords)

		faceCliquee = self.canv.find_withtag("current") # id du polygone sur lequel on a clique
		if(self.canv.type(faceCliquee) == "polygon"):

			idCube = int(self.canv.gettags(faceCliquee)[0].split("_")[1]) # tag 0 : "cube_idfaceduhaut"
			for cube in self.CUBES: # on teste chaque cube deja place
				if cube.id == idCube: # si c'est celui sur lequel on a clique
					x,y = self.grille.canvasToGrille(cube.coords) # coordonnees 2D "reelles" du cube dans la grille

					position3D = (x+cube.h,y+cube.h,cube.h) # on obtient les coordonnees de hauteur 0 (case de base), et la hauteur

					# on teste les id de faces pour savoir laquelle c'etait ; faceCliquee[0] car c'est un tuple
					if faceCliquee[0] == cube.haut:
						print("on place le cube sur la face haut")
						self.placerCubeHaut(position3D)
					elif faceCliquee[0] == cube.gauche:
						print("on place le cube sur la face gauche")
						self.placerCubeGauche(position3D)
					elif faceCliquee[0] == cube.droite:
						print("on place le cube sur la face droite")
						self.placerCubeDroite(position3D)
					break
		
		# sinon on a clique sur la grille
		elif convertedCoords[0] < self.grille.taille_x and convertedCoords[1] < self.grille.taille_y and convertedCoords[0] > 0 and convertedCoords[1] > 0:
			# il faut supprimer la limite de placement en vertical vers le haut, sinon on peut pas faire + de 1 cube en (0,0)
			hauteur = 0
			self.placerCube((convertedCoords[0]-0.5,convertedCoords[1]-0.5),hauteur) # on ajuste le point 0.5 case plus haut

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
		self.deroulFichier.add_command(label="Charger", command=self.ouvrirFichier)
		self.deroulFichier.add_command(label="Sauver", command=self.sauverFichier)
		self.deroulFichier.add_command(label="Annuler", command=self.annulerDernierCube)
		self.root.bind("<Control-z>", self.annulerDernierCube)

		# on desactive les options annuler et sauver
		self.deroulFichier.entryconfigure(2,state="disabled")
		self.deroulFichier.entryconfigure(3,state="disabled")

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
