import tkinter as tk
import Grille
import Cube
from tkinter import filedialog,messagebox

import time # a supp

class App:

	# DICO : contient la position 3D de tous les cubes sous la forme DICO[(x,y)] = [hauteur_1,hauteur_2...]
	DICO = {}

	CUBES = [] # liste des cubes places
	__couleur_cube = ["#afafaf","#808080","#414141"] # couleur des cubes par defaut
	COULEUR_MAX = 16777215 # la couleur #ffffff en decimal

	precoords = () # Tuple pour memoriser les coordonnees precedentes pour le previsualisation

	# Exportation en .SVG

	def dessinerGrilleSVG(self, pfichier):
		# Fonction qui ecrit dans un fichier SVG et qui pose des balises <line> pour dessiner la grille avec des lignes
		x = self.grille.origine[0]
		y = self.grille.origine[1]
		d = self.grille.definition
		# c'est en realite la meme methode que dans Grille.dessinegrille()
		for i in range(self.grille.taille_y+1):
			pfichier.write("<line x1=\"" + str(x) + "\" " + "x2=\"" + str(x+d*self.grille.taille_y) + "\" " + "y1=\"" + str(y) + "\" " + "y2=\"" + str(y+(d*self.grille.taille_y/2)) + "\"")
			x -= d
			y += d/2
			pfichier.write(" stroke=\"grey\"")
			pfichier.write("/>\n")
		x = self.grille.origine[0]
		y = self.grille.origine[1]
		for j in range(self.grille.taille_x+1):
			pfichier.write("<line x1=\"" + str(x) + "\" " + "x2=\"" + str(x-d*self.grille.taille_y) + "\" " + "y1=\"" + str(y) + "\" " + "y2=\"" + str(y+(d*self.grille.taille_y/2)) + "\"")
			x += d
			y += d/2
			pfichier.write(" stroke=\"grey\"")
			pfichier.write("/>\n")

	def dessinerCubeSVG(self,pcoordsGrille,pfichier,phauteur,pcouleur=__couleur_cube):
		# Fonction qui ecrit dans un fichier SVG et qui pose des balises <polygon> pour dessiner les cubes
		d = self.grille.definition
		canv_coords = self.grille.grilleToCanvas(pcoordsGrille)
		x = canv_coords[0]
		y = canv_coords[1]
		# c'est en realite la meme methode que dans Cube.dessiner()
		pfichier.write("<polygon points=\"")
		# Face Haut
		pfichier.write(str(x) + " " + str(y) + "," + str(x+d)+ " " + str(y-d/2) + "," + str(x) + " " + str(y-d) + "," + str(x-d) + " " + str(y-d/2))
		pfichier.write("\"")
		pfichier.write(f" stroke=\"black\" fill=\"{pcouleur[0]}\" />\n")
		# Face Gauche
		pfichier.write("<polygon points=\"")
		pfichier.write(str(x) + " " + str(y) + "," + str(x-d)+ " " + str(y-d/2) + "," + str(x-d) + " " + str(y+d/2) + "," + str(x) + " " + str(y+d))
		pfichier.write("\"")
		pfichier.write(f" stroke=\"black\" fill=\"{pcouleur[1]}\" />\n")
		# Face Droite
		pfichier.write("<polygon points=\"")
		pfichier.write(str(x) + " " + str(y) + "," + str(x+d)+ " " + str(y-d/2) + "," + str(x+d) + " " + str(y+d/2) + "," + str(x) + " " + str(y+d))
		pfichier.write("\"")
		pfichier.write(f" stroke=\"black\" fill=\"{pcouleur[2]}\" />\n")

	def sauverSVG(self):
		# Fonction qui ouvre un fichier SVG et qui dessine le projet actuel
		fichier = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=(("SVG files", ".svg"),("All files", ".*")))
		try:
			with open(fichier, "w", encoding = "utf-8") as f:
				# Ecriture du header xml, puis d'une viewbox, qui est en realite comme notre canvas
				f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
				f.write("<svg viewBox=" + "\"0 0 " + str(self.canv.cget("width")) + " " + str(self.canv.cget("height")) + "\" " + "xmlns=\"http://www.w3.org/2000/svg\">\n")
				self.dessinerGrilleSVG(f)
				# pas optimise, mais facultatif
				liste = self.canv.find_all()[self.grille.taille_x+self.grille.taille_y+2:] # a partir du nb de lignes+1 jusqu'a la fin : les faces des cubes
				# attention : les id commencent a 1
				for i in range(len(liste)):
					if i%3 == 0: # verifier si ça fonctionne toujours avec les pixmaps
						# on a un id de cube, il nous faut l'objet pour avoir ses coordonnees
						for c in self.CUBES:
							print("c.id :",c.id,"liste[i] :",liste[i])
							if c.id == liste[i]:
								cube = c
								print("	cube id trouvé :",cube.id,"; coords :",cube.coords)
								break
						# cube est le cube correspondant a l'id i
						coords2D = self.grille.canvasToGrille(cube.coords)
						self.dessinerCubeSVG(coords2D,f,cube.h,cube.couleur)
				f.write("</svg>")
		except: # Si il y a une erreur, le dire a l'utilisateur, (gerer les differentes erreurs apres !!!!)
			messagebox.showerror(title="Error", message="Erreur lors de l'ouverture du fichier.")
			# attention : appele aussi quand l'utilisateur clique sur Annuler


	# Conservation des donnees

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
		self.deroulFichier.entryconfigure(2,state="disabled") # option Exporter
		self.deroulFichier.entryconfigure(3,state="disabled") # option Sauver
		self.deroulFichier.entryconfigure(4,state="disabled") # option Annuler

	def sauverFichier(self):
		fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", ".txt"),("All files", ".*"))) # On demande a l'utilisateur dans quel fichier il veut sauver le projet
		try: # On ecrit dans le fichier les coordonnees et couleurs des cubes
			with open(fichier, "w", encoding = "utf-8") as f:
				for cube in self.CUBES:
					coords_grille = self.grille.closestPoint(self.grille.canvasToGrille(cube.coords))
					coords3D = (coords_grille[0]+cube.h,coords_grille[1]+cube.h)
					couleur_faces = cube.couleur
					f.write(f"{coords3D[0]},{coords3D[1]},{cube.h},{couleur_faces[0]},{couleur_faces[1]},{couleur_faces[2]}\n")
					# f.write()
					# f.write(str(pos_cube[0]) + "," + str(pos_cube[1]) + " ")
		except: # Si il y a une erreur, le dire a l'utilisateur, (gerer les differentes erreurs apres !!!!)
			messagebox.showerror(title="Error", message="Erreur lors de l'ouverture du fichier.")
			# attention : appele aussi quand l'utilisateur clique sur Annuler

	def ouvrirFichier(self):
		self.nouveauFichier()
		fichier = filedialog.askopenfile(mode="r",defaultextension=".txt", filetypes=(("Text files", ".txt"),("All files", ".*")))
		if(fichier):
			for ligne in fichier.readlines():
				parse = ligne.rstrip().split(',')
				self.placerCube((int(parse[0]),int(parse[1])),int(parse[2]),parse[3:6])
			fichier.close()


	# Manipulation des cubes

	def annulerDernierCube(self,event=None):
		"""Annule le dernier placement de cube."""
		# le parametre event est obligatoire pour etre bind
		if len(self.CUBES) == 1:
			self.deroulFichier.entryconfigure(2,state="disabled") # option Sauver
			self.deroulFichier.entryconfigure(3,state="disabled") # option Annuler
		if len(self.CUBES) > 0:
			cube = self.CUBES[-1]
			coordsGrille = self.grille.canvasToGrille(cube.coords)
			self.DICO[(coordsGrille[0]+cube.h,coordsGrille[1]+cube.h)].pop()
			if(self.DICO[(coordsGrille[0]+cube.h,coordsGrille[1]+cube.h)] == []):
				del self.DICO[(coordsGrille[0]+cube.h,coordsGrille[1]+cube.h)]
			self.CUBES[-1].effacer(self.canv)
			self.CUBES.pop()
		else:
			print("plus de cubes dans la liste")

	def placerCube(self,pcoordsGrille,phauteur,pcouleur=None):
		"""
		Prend en parametre des coordonnees de self.grille, comme (2.125, 4.08) (peut-etre a changer ?)
		Attention : recale la position au point le plus proche (closestPoint)
		"""
		coords3D = self.grille.closestPoint(pcoordsGrille) # coordonnees de la case ou est place le cube
		self.addCubeToDico(coords3D,phauteur) # coordonnees reelles du cube, sur une case de la grille mais en hauteur

		# on transforme les coordonnees 3D en coordonnees 2D "aplaties", transposees "comme on les voit", sans hauteur
		coordsGrille = (coords3D[0]-phauteur,coords3D[1]-phauteur)
		if not(pcouleur):
			pcouleur = self.__couleur_cube
		cube = Cube.Cube(self.canv,self.grille,coordsGrille,phauteur,pcouleur)
		# print("  placed cube",cube.id,"at :",(*pcoordsGrille,phauteur),"--",str(coordsGrille)) # coords 3D puis 2D

		indexCube = self.canv.find_all().index(cube.id) # index de la face du haut dans la liste de tous les elements du canvas

		tag = "cube_"+str(cube.id) # on a le tag "cube_idfaceduhaut", associe a toutes les faces du nouveau cube
		for autreCube in self.CUBES:
			if autreCube == cube:
				continue
			indexCube = self.canv.find_all().index(cube.id) # index de la face du haut dans la liste de tous les elements du canvas

			autreIndex = self.canv.find_all().index(autreCube.id)

			# on utilise le meme procede que prededemment pour avoir les coordonnees du cube analyse
			autreCoordsGrille = self.grille.closestPoint(self.grille.canvasToGrille(autreCube.coords))
			autreCoords3D = (autreCoordsGrille[0]+autreCube.h,autreCoordsGrille[1]+autreCube.h)

			if phauteur > autreCube.h and autreIndex > indexCube: # si le nouveau cube est plus haut mais que l'autre cube est dessine plus haut
				self.canv.tag_raise(tag,(autreCube.id+2)) # +2 car on doit placer le cube au dessus de toutes les faces de l'autre cube
			elif phauteur < autreCube.h and autreIndex < indexCube:
				self.canv.tag_lower(tag,autreCube.id) # le nouveau est plus bas
			# a chaque fois il faut regarder l'ordre de dessin : si la condition est fausse, c'est que le cube est deja bien place
			elif phauteur == autreCube.h:
				# on ne peut pas rassembler les deux conditions car ce ne sont pas exactement les memes
				if coords3D[0] >= autreCoords3D[0]:
					if coords3D[1] >= autreCoords3D[1] and autreIndex > indexCube:
						self.canv.tag_raise(tag,(autreCube.id+2))
					elif coords3D[1] < autreCoords3D[1] and autreIndex < indexCube:
						self.canv.tag_lower(tag,autreCube.id)
				elif coords3D[0] < autreCoords3D[0]:
					if coords3D[1] > autreCoords3D[1] and autreIndex > indexCube:
						self.canv.tag_raise(tag,(autreCube.id+2))
					elif coords3D[1] <= autreCoords3D[1] and autreIndex < indexCube:
						self.canv.tag_lower(tag,autreCube.id)


		self.CUBES.append(cube)
		# on active les options d'exportation, de sauvegarde et d'annulation
		self.deroulFichier.entryconfigure(2,state="normal")
		self.deroulFichier.entryconfigure(3,state="normal")
		self.deroulFichier.entryconfigure(4,state="normal")
		return cube # ne sert a rien pour l'instant, mais au cas ou

	def placerCubeHaut(self,pposition3D):
		"""Place un cube en haut de la position 3D passee en parametre (x,y,hauteur)"""
		x,y,h = pposition3D
		return self.placerCube((x,y),h+1)

	def placerCubeGauche(self,pposition3D):
		"""Place un cube a gauche de la position 3D passee en parametre (x,y,hauteur)"""
		x,y,h = pposition3D
		return self.placerCube((x,y+1),h)

	def placerCubeDroite(self,pposition3D):
		"""Place un cube a droite de la position 3D passee en parametre (x,y,hauteur)"""
		x,y,h = pposition3D
		return self.placerCube((x+1,y),h)

	# Interface de choix de la couleur

	def calculerTriplet(self,nombre):
		B = nombre % 256
		V = (nombre // 256) % 256
		R = ((nombre // 256) // 256) % 256
		return (R,V,B)

	def hex2dec(self,code):
		"""Convertit un code hexadecimal (commançant par #) en tuple d'entiers"""
		return [ int(code[j:j+2],16) for j in range(1,7,2) ]

	def dec2hex(self,triplet):
		"""
		Convertit le tuple d'entiers donne en parametre
		en chaine de caractere representant la couleur en hexadecimal
		"""
		res = "#"
		for i in range(3):
			hexa = hex(triplet[i])[2:]
			if(len(hexa) < 2): # les nb < 16 font 1 seul caractere, on en veut 2
				hexa = "0"+hexa
			res += hexa
		return res

	def ouvrirFenetreCouleur(self):
		"""Ouvre la fenetre de selection des couleurs pour un cube"""

		self.__fenetre_couleur = tk.Toplevel(self.root)
		
		# Visualisation du cube a gauche
		self.__canvas_couleur = tk.Canvas(self.__fenetre_couleur,width=160,height=100) # a equilibrer
		self.__canvas_couleur.pack(side=tk.LEFT)

		grille_couleur = Grille.Grille(self.__canvas_couleur,25,1,1,porigine=(80,50)) # d = 10, taille_x,taille_y = 1,1
		self.__cube_couleur = Cube.Cube(self.__canvas_couleur,grille_couleur,(0,0),phauteur=0,pcouleur=self.__couleur_cube)

		# Initialisation des Frames
		frame_couleur_right = tk.Frame(self.__fenetre_couleur)
		frame_couleur_right.pack(side=tk.TOP)
		frame_couleur_RVB = tk.Frame(frame_couleur_right)
		frame_couleur_RVB.pack(side=tk.TOP,anchor="nw")

		frame_couleur_haut = tk.Frame(frame_couleur_right)
		frame_couleur_haut.pack(side=tk.TOP)
		frame_couleur_gauche = tk.Frame(frame_couleur_right)
		frame_couleur_gauche.pack(side=tk.TOP)
		frame_couleur_droite = tk.Frame(frame_couleur_right)
		frame_couleur_droite.pack(side=tk.TOP)

		bottom_frame_couleur = tk.Frame(self.__fenetre_couleur)
		bottom_frame_couleur.pack(side=tk.BOTTOM)
		
		# Codes couleur synchronises avec les sliders
		# Codes en hexadecimal
		self.__stringvar_couleur_haut = tk.StringVar(value=self.__couleur_cube[0])
		self.__stringvar_couleur_gauche = tk.StringVar(value=self.__couleur_cube[1])
		self.__stringvar_couleur_droite = tk.StringVar(value=self.__couleur_cube[2])

		# Valeurs decimales, calculees grace aux codes hexa
		self.__code_couleur_haut_RVB = tk.IntVar(value=int(self.__stringvar_couleur_haut.get()[1:],16))
		self.__code_couleur_gauche_RVB = tk.IntVar(value=int(self.__stringvar_couleur_gauche.get()[1:],16))
		self.__code_couleur_droite_RVB = tk.IntVar(value=int(self.__stringvar_couleur_droite.get()[1:],16))

		# Affichage des codes dans des Entries
		label_couleur_texte = tk.Label(frame_couleur_RVB,text="  R :     V :     B :    code hex :")
		label_couleur_texte.pack()
		
		triplets = [self.calculerTriplet(self.__code_couleur_haut_RVB.get()),
					self.calculerTriplet(self.__code_couleur_gauche_RVB.get()),
					self.calculerTriplet(self.__code_couleur_droite_RVB.get())]

		couleur_haut_entry_R = tk.Entry(frame_couleur_haut,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_haut_entry_V = tk.Entry(frame_couleur_haut,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_haut_entry_B = tk.Entry(frame_couleur_haut,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		self.__couleur_haut_entry_RVB = [couleur_haut_entry_R, couleur_haut_entry_V, couleur_haut_entry_B]
		for i in range(3):
			self.__couleur_haut_entry_RVB[i].insert(tk.END,str(triplets[0][i]))
			self.__couleur_haut_entry_RVB[i].pack(side=tk.LEFT)

		couleur_gauche_entry_R = tk.Entry(frame_couleur_gauche,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_gauche_entry_V = tk.Entry(frame_couleur_gauche,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_gauche_entry_B = tk.Entry(frame_couleur_gauche,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		self.__couleur_gauche_entry_RVB = [couleur_gauche_entry_R, couleur_gauche_entry_V, couleur_gauche_entry_B]
		for i in range(3):
			self.__couleur_gauche_entry_RVB[i].insert(tk.END,str(triplets[1][i]))
			self.__couleur_gauche_entry_RVB[i].pack(side=tk.LEFT)
		
		couleur_droite_entry_R = tk.Entry(frame_couleur_droite,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_droite_entry_V = tk.Entry(frame_couleur_droite,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		couleur_droite_entry_B = tk.Entry(frame_couleur_droite,width=4,justify=tk.CENTER) # il faudrait empecher les txt + longs que 3
		self.__couleur_droite_entry_RVB = [couleur_droite_entry_R, couleur_droite_entry_V, couleur_droite_entry_B]
		for i in range(3):
			self.__couleur_droite_entry_RVB[i].insert(tk.END,str(triplets[2][i]))
			self.__couleur_droite_entry_RVB[i].pack(side=tk.LEFT)

		couleur_haut_hexa_entry = tk.Entry(frame_couleur_haut,width=10,justify=tk.CENTER,textvariable=self.__stringvar_couleur_haut) # il faudrait rajouter la possiblite d'ecrire la couleur
		couleur_gauche_hexa_entry = tk.Entry(frame_couleur_gauche,width=10,justify=tk.CENTER,textvariable=self.__stringvar_couleur_gauche) # il faudrait rajouter la possiblite d'ecrire la couleur
		couleur_droite_hexa_entry = tk.Entry(frame_couleur_droite,width=10,justify=tk.CENTER,textvariable=self.__stringvar_couleur_droite) # il faudrait rajouter la possiblite d'ecrire la couleur

		for entry in (couleur_haut_hexa_entry,couleur_gauche_hexa_entry,couleur_droite_hexa_entry):
			entry.pack(side=tk.LEFT)

		# Sliders affiches en bas
		# Note : modifier une variable liee n'appelle pas le callback, utile pour modifier toutes les scales en meme temps
		# (https://stackoverflow.com/questions/4038517/tkinter-set-a-scale-value-without-triggering-callback)
		scale_couleur_haut = tk.Scale(bottom_frame_couleur,orient="horizontal", from_=0, to=self.COULEUR_MAX,
									command=self.updateCouleurHaut, showvalue=0, resolution=1, length=200,
									variable=self.__code_couleur_haut_RVB).pack() # length a equilibrer
		scale_couleur_gauche = tk.Scale(bottom_frame_couleur,orient="horizontal", from_=0, to=self.COULEUR_MAX,
									command=self.updateCouleurGauche, showvalue=0, resolution=1, length=200,
									variable=self.__code_couleur_gauche_RVB).pack()
		scale_couleur_droite = tk.Scale(bottom_frame_couleur,orient="horizontal", from_=0, to=self.COULEUR_MAX,
									command=self.updateCouleurDroite, showvalue=0, resolution=1, length=200,
									variable=self.__code_couleur_droite_RVB).pack()


		# Mode automatique
		self.__mode_auto = tk.BooleanVar(value=True) # definit le comportement des sliders : mis a jour automatiquement (True) ou separement (False)
		couleur_check_mode_auto = tk.Checkbutton(bottom_frame_couleur,text="Modifier ensemble",variable=self.__mode_auto)
		couleur_check_mode_auto.pack(side=tk.LEFT)

		# Confirmer
		couleur_bouton_ok = tk.Button(bottom_frame_couleur,text="Ok",command=self.confirmerCouleur)
		couleur_bouton_ok.pack(side=tk.RIGHT,padx=10)

	def confirmerCouleur(self):
		self.__couleur_cube = [self.__stringvar_couleur_haut.get(),	self.__stringvar_couleur_gauche.get(), self.__stringvar_couleur_droite.get()]
		self.__fenetre_couleur.destroy()

	# Gestion d'evenements

	def onMotion(self, event):
		d = self.grille.definition
		coordsEvent = (event.x,event.y)
		coordsGrille = self.grille.canvasToGrille(coordsEvent)

		if(self.cubeTest == None):
			# On cree le cube qui sera celui de la previsualisation
			if(self.grille.is_in_grille(coordsEvent)):
				self.cubeTest = Cube.Cube(self.canv,self.grille,coordsGrille,0,pcouleur=("#f2e6e3","#f2e6e3","#f2e6e3")) # On place le cube si l'utilisateur entre dans la grille
				self.cubeTest.disable(self.canv) # on met le cube et disabled pour qu'on ne puisse par cliquer dessus
				self.precoords = coordsEvent
		else:
			currentFace = self.canv.find_withtag("current") # id du polygone sur lequel on est
			new_coords = self.grille.grilleToCanvas(self.grille.closestPointUp(self.grille.canvasToGrille(coordsEvent)))
			if(self.canv.type(currentFace) == "polygon"): # si on a est bien sur un polygone (une face de cube)
				idCube = int(self.canv.gettags(currentFace)[0].split("_")[1]) # tag 0 : "cube_idfaceduhaut"
				for cube in self.CUBES: # on teste chaque cube deja place
					if cube.id == idCube: # si c'est celui sur lequel on est
						x,y = self.grille.canvasToGrille(cube.coords) # coordonnees 2D "reelles" du cube dans la grille
						# on teste les id de faces pour savoir laquelle c'etait ; currentFace[0] car c'est un tuple
						# on adapte la position en fonction de la face courante
						if currentFace[0] == cube.haut:
							x -= 1
							y -= 1
						elif currentFace[0] == cube.gauche:
							y += 1
						elif currentFace[0] == cube.droite:
							x +=1

						new_coords2 = self.grille.grilleToCanvas((x,y))
						delta_x = new_coords2[0] - self.precoords[0]
						delta_y = new_coords2[1] - self.precoords[1]
						self.canv.move("cube_"+str(self.cubeTest.id), delta_x,delta_y)
						self.precoords = new_coords2
						break

			elif self.grille.is_in_grille(coordsEvent):
				delta_x = new_coords[0] - self.precoords[0]
				delta_y = new_coords[1] - self.precoords[1]

				self.precoords = new_coords
				self.canv.move("cube_"+str(self.cubeTest.id), delta_x,delta_y)

	def onClick(self,event):
		"""En cas de clic sur le canvas"""
		currentCoords = (event.x,event.y)
		convertedCoords = self.grille.canvasToGrille(currentCoords)
		# print("click on :",currentCoords,"=>",convertedCoords)

		faceCliquee = self.canv.find_withtag("current") # id du polygone sur lequel on a clique

		if(self.canv.type(faceCliquee) == "polygon"): # si on a bien clique sur un polygone (une face de cube)
			idCube = int(self.canv.gettags(faceCliquee)[0].split("_")[1]) # tag 0 : "cube_idfaceduhaut"
			for cube in self.CUBES: # on teste chaque cube deja place
				if cube.id == idCube: # si c'est celui sur lequel on a clique
					x,y = self.grille.canvasToGrille(cube.coords) # coordonnees 2D "reelles" du cube dans la grille

					position3D = (x+cube.h,y+cube.h,cube.h) # on obtient les coordonnees de hauteur 0 (case de base), et la hauteur

					# on teste les id de faces pour savoir laquelle c'etait ; faceCliquee[0] car c'est un tuple
					if faceCliquee[0] == cube.haut:
						self.placerCubeHaut(position3D)
					elif faceCliquee[0] == cube.gauche:
						self.placerCubeGauche(position3D)
					elif faceCliquee[0] == cube.droite:
						self.placerCubeDroite(position3D)
					break

		elif self.grille.is_in_grille(currentCoords):
			# sinon ce n'est pas un polygone alors on a clique autre part : on regarde si c'est dans la grille
			# il faut supprimer la limite de placement en vertical vers le haut, sinon on peut pas faire + de 1 cube en (0,0)
			hauteur = 0
			self.placerCube(self.grille.closestPointUp(convertedCoords),hauteur) # on ajuste le point 0.5 case plus haut
		if(self.cubeTest):
			self.cubeTest.priorite(self.canv)

	def updateCouleurHaut(self,valeur):
		"""
		On modifie les variables self.__couleur_* pour qu'elles correspondent aux valeurs
		des sliders de selection de couleur. On met aussi a jour la couleur des faces du cube.
		"""
		val = int(valeur)
		triplet_haut = self.calculerTriplet(val)
		code = self.dec2hex(triplet_haut)
		
		self.__stringvar_couleur_haut.set(code)
		
		nouvelle_couleur = [code,None,None]
		
		# si le mode automatique est actif, on modifie les autres faces
		# les couleurs automatiques ne sont pas parfaites, mais dans certains cas ça marche plutot bien
		if(self.__mode_auto.get()):
			nouvelle_couleur[1] = self.dec2hex(self.calculerTriplet(int(0.73142*val)))
			nouvelle_couleur[2] = self.dec2hex(self.calculerTriplet(int(0.37142*val)))

			# codes RVB
			self.__stringvar_couleur_gauche.set(nouvelle_couleur[1]) # valeurs calculees (precision arbitraire)
			self.__stringvar_couleur_droite.set(nouvelle_couleur[2])
			
			# codes hexa
			self.__code_couleur_gauche_RVB.set(int(nouvelle_couleur[1][1:],16))
			self.__code_couleur_droite_RVB.set(int(nouvelle_couleur[2][1:],16))

			for i in range(3):
				# on modifie chaque entry pour la face, en fonction du code en hexadecimal
				triplet_temp = self.hex2dec(nouvelle_couleur[1])
				self.__couleur_gauche_entry_RVB[i].delete(0,tk.END)
				self.__couleur_gauche_entry_RVB[i].insert(tk.END,triplet_temp[i])
			for i in range(3):
				triplet_temp = self.hex2dec(nouvelle_couleur[2])
				self.__couleur_droite_entry_RVB[i].delete(0,tk.END)
				self.__couleur_droite_entry_RVB[i].insert(tk.END,triplet_temp[i])

		else:
			nouvelle_couleur[1] = self.__stringvar_couleur_gauche.get()
			nouvelle_couleur[2] = self.__stringvar_couleur_droite.get()
		# dans tous les cas, on change la couleur du cube
		self.__cube_couleur.changerCouleur(self.__canvas_couleur,nouvelle_couleur)
		# pour chaque face, on modifie l'entry correspondante, en fonction du code en hexadecimal
		for i in range(3):
			self.__couleur_haut_entry_RVB[i].delete(0,tk.END)
			self.__couleur_haut_entry_RVB[i].insert(tk.END,triplet_haut[i])

	def updateCouleurGauche(self,valeur):
		val = int(valeur)
		triplet_gauche = self.calculerTriplet(val)
		code = self.dec2hex(triplet_gauche)

		self.__stringvar_couleur_gauche.set(code)

		nouvelle_couleur = [None,code,None]
		
		if(self.__mode_auto.get()):
			nouvelle_couleur[0] = self.dec2hex(self.calculerTriplet(int(2.6923*val)))
			nouvelle_couleur[2] = self.dec2hex(self.calculerTriplet(int(1.9692*val)))

			# codes RVB
			self.__stringvar_couleur_haut.set(nouvelle_couleur[0])
			self.__stringvar_couleur_droite.set(nouvelle_couleur[2]) # valeurs calculees (precision arbitraire)

			# codes hexa
			self.__code_couleur_haut_RVB.set(int(nouvelle_couleur[0][1:],16))
			self.__code_couleur_droite_RVB.set(int(nouvelle_couleur[2][1:],16))

			# on met a jour les Entry des autres faces
			triplet_temp = self.hex2dec(nouvelle_couleur[0])
			for i in range(3):
				# on modifie chaque entry pour la face, en fonction du code en hexadecimal
				self.__couleur_haut_entry_RVB[i].delete(0,tk.END)
				self.__couleur_haut_entry_RVB[i].insert(tk.END,triplet_temp[i])
			triplet_temp = self.hex2dec(nouvelle_couleur[2])
			for i in range(3):
				self.__couleur_droite_entry_RVB[i].delete(0,tk.END)
				self.__couleur_droite_entry_RVB[i].insert(tk.END,triplet_temp[i])

		else:
			nouvelle_couleur[0] = self.__stringvar_couleur_haut.get()
			nouvelle_couleur[2] = self.__stringvar_couleur_droite.get()
		# dans tous les cas, on change la couleur du cube
		self.__cube_couleur.changerCouleur(self.__canvas_couleur,nouvelle_couleur)
		# pour chaque face, on modifie l'entry correspondante, en fonction du code en hexadecimal
		for i in range(3):
			self.__couleur_gauche_entry_RVB[i].delete(0,tk.END)
			self.__couleur_gauche_entry_RVB[i].insert(tk.END,triplet_gauche[i])

	def updateCouleurDroite(self,valeur):
		val = int(valeur)
		triplet_droite = self.calculerTriplet(val)
		code_hexa = self.dec2hex(triplet_droite)

		self.__stringvar_couleur_droite.set(code_hexa)

		nouvelle_couleur = [None,None,code_hexa]
		
		if(self.__mode_auto.get()):
			nouvelle_couleur[0] = self.dec2hex(self.calculerTriplet(int(2.6923*val))) # (precision arbitraire)
			nouvelle_couleur[1] = self.dec2hex(self.calculerTriplet(int(1.9692*val)))
			
			# codes RVB
			self.__stringvar_couleur_haut.set(nouvelle_couleur[0])
			self.__stringvar_couleur_gauche.set(nouvelle_couleur[1])

			# codes hexa
			self.__code_couleur_haut_RVB.set(int(nouvelle_couleur[0][1:],16))
			self.__code_couleur_gauche_RVB.set(int(nouvelle_couleur[1][1:],16))

			# mise a jour des Entry des autres faces
			triplet_temp = self.hex2dec(nouvelle_couleur[0])
			for i in range(3):
				self.__couleur_haut_entry_RVB[i].delete(0,tk.END)
				self.__couleur_haut_entry_RVB[i].insert(tk.END,triplet_temp[i])
			triplet_temp = self.hex2dec(nouvelle_couleur[1])
			for i in range(3):
				self.__couleur_gauche_entry_RVB[i].delete(0,tk.END)
				self.__couleur_gauche_entry_RVB[i].insert(tk.END,triplet_temp[i])

		else:
			# sinon, on modifie seulement l'actuelle
			nouvelle_couleur[0] = self.__stringvar_couleur_haut.get()
			nouvelle_couleur[1] = self.__stringvar_couleur_gauche.get()
		
		# dans tous les cas, on change la couleur du cube
		self.__cube_couleur.changerCouleur(self.__canvas_couleur,nouvelle_couleur)
		# pour chaque face, on modifie l'entry correspondante, en fonction du code en hexadecimal
		for i in range(3):
			self.__couleur_droite_entry_RVB[i].delete(0,tk.END)
			self.__couleur_droite_entry_RVB[i].insert(tk.END,triplet_droite[i])


	# Constructeur de l'application

	def __init__(self):

		# Root
		self.root = tk.Tk()

		# Menus

		self.menuFrame = tk.Frame(self.root,bg="red") # ne pas oublier d'enlever le bg
		self.menuFrame.pack(side=tk.TOP,expand=True,fill=tk.X,anchor="n")

		self.bottomFrame = tk.Frame(self.root,bg="blue")
		self.bottomFrame.pack(side=tk.BOTTOM,expand=True,fill=tk.X,anchor="s")

		# Menu fichier
		self.menuFichier = tk.Menubutton(self.menuFrame,text="Fichier",underline=0,relief="raised")

		self.deroulFichier = tk.Menu(self.menuFichier, tearoff=False)
		self.deroulFichier.add_command(label="Nouveau", command=self.nouveauFichier)
		self.deroulFichier.add_command(label="Charger", command=self.ouvrirFichier)
		self.deroulFichier.add_command(label="Exporter", command=self.sauverSVG)
		self.deroulFichier.add_command(label="Sauver", command=self.sauverFichier)
		self.deroulFichier.add_command(label="Annuler", command=self.annulerDernierCube)
		self.root.bind("<Control-z>", self.annulerDernierCube)
		self.visualiser = tk.BooleanVar(value=False)
		self.deroulFichier.add_checkbutton(label="Visualiser", variable=self.visualiser)
		self.deroulFichier.add_command(label="Couleur", command=self.ouvrirFenetreCouleur)

		# on desactive les options annuler et sauver
		self.deroulFichier.entryconfigure(2,state="disabled")
		self.deroulFichier.entryconfigure(3,state="disabled")
		self.deroulFichier.entryconfigure(4,state="disabled")

		# self.deroulFichier.add_command(label="Quitter", command=quitApp)
		# self.root.protocol("WM_DELETE_WINDOW", quitApp) # pour gerer la fermeture avec la croix rouge et alt-f4


		self.menuFichier.config(menu=self.deroulFichier)
		self.menuFichier.pack(side=tk.LEFT)

		# Menu aide

		self.menuAide = tk.Menubutton(self.menuFrame,text="Aide",underline=0,relief="raised")

		self.derouleAide = tk.Menu(self.menuAide,tearoff=False)

		self.menuAide.config(menu=self.derouleAide)
		self.menuAide.pack(side=tk.RIGHT)

		# Canvas

		self.canv = tk.Canvas(self.root,width=500,height=500,bg="white")
		self.canv.bind("<Motion>",self.onMotion)
		self.canv.bind("<Button-1>",self.onClick)

		self.grille = Grille.Grille(self.canv)
		self.cubeTest = None
		# cube1 = Cube.Cube(self.canv,self.grille,(1,1))

		self.canv.pack()


		# Fin

		self.root.mainloop()


App()

exit(0)
