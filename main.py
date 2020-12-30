import tkinter as tk
import Grille
import Cube
from tkinter import filedialog,messagebox
import webbrowser # Pour la documentation

class App:

	# DICO : contient la position 3D de tous les cubes sous la forme DICO[(x,y)] = [hauteur_1,hauteur_2...]
	DICO = {}

	CUBES = [] # liste des cubes places
	__couleur_cube = ["#afafaf","#808080","#414141"] # couleur des cubes par defaut
	COULEUR_MAX = 16777215 # la couleur #ffffff en decimal

	cube_select = None
	NB_CUBES = 0 # Pour savoir combien il y a de cubes dans la scene, et pour leur attribuer des numeros
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
				liste = self.canv.find_all()[self.grille.taille_x+self.grille.taille_y+3:] # a partir du nb de lignes+1 jusqu'a la fin : les faces des cubes
				# attention : les id commencent a 1
				for i in range(0,len(liste),3):
					if liste[i] != self.cubeTest.id: # verifier si ça fonctionne toujours avec les pixmaps (autres types de polygones peut-etre ?)
						# on a un id de cube, il nous faut l'objet pour avoir ses coordonnees
						for c in self.CUBES:
							# print("c.id :",c.id,"; liste[i] :",liste[i])
							if c.id == liste[i]:
								cube = c
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

	def insererDansDisplayList(self,pcube):
		"""
		Permet d'inserer un cube dans la display list
		a la bonne position, avec la bonne perspective
		"""
		coords3D = pcube.coordsTo3D()
		indexCube = self.canv.find_all().index(pcube.id) # index de la face du haut dans la liste de tous les elements du canvas

		tag = "cube_"+str(pcube.id) # on a le tag "cube_idfaceduhaut", associe a toutes les faces du nouveau cube
		for autreCube in self.CUBES:
			if autreCube == pcube:
				continue
			
			displayList = self.canv.find_all()

			indexCube = displayList.index(pcube.id) # index de la face du haut dans la liste de tous les elements du canvas
			autreIndex = displayList.index(autreCube.id)

			# on utilise le meme procede que dans placerCube() pour avoir les coordonnees du cube analyse
			autreCoords3D = autreCube.coordsTo3D()

			if pcube.h > autreCube.h and autreIndex > indexCube: # si le nouveau cube est plus haut mais que l'autre cube est dessine plus haut
				self.canv.tag_raise(tag,(autreCube.id+2)) # +2 car on doit placer le cube au dessus de toutes les faces de l'autre cube
			elif pcube.h < autreCube.h and autreIndex < indexCube:
				self.canv.tag_lower(tag,autreCube.id) # le nouveau est plus bas
			# a chaque fois il faut regarder l'ordre de dessin : si la condition est fausse, c'est que le cube est deja bien place
			elif pcube.h == autreCube.h:
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


	def nouveauFichier(self):
		self.NB_CUBES = 0
		self.canv.itemconfigure(self.texte_cubes, text="Nombre de cubes dans la scene: "+str(self.NB_CUBES))
		# on efface tous les cubes
		for cube in self.CUBES:
			cube.effacer()
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
					coords3D = cube.coordsTo3D()
					couleur_faces = cube.couleur
					f.write(f"{int(coords3D[0])},{int(coords3D[1])},{cube.h},{couleur_faces[0]},{couleur_faces[1]},{couleur_faces[2]}\n")
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

	def rechercherCube(self,pid):
		''' A partir d'un id, la fonction renvoie l'objet cube correspondant a cet id'''
		for cube in self.CUBES: # on teste chaque cube deja place
			if cube.id == pid: # si c'est celui sur lequel on a clique
				return(cube)
		return(None)

	def translationCube(self,pcube,pcoords3D):
		"""Deplace un cube a la position (tuple de longueur 3) passee en parametre, inconditionnellement."""
		prec_x,prec_y = self.grille.closestPoint(pcube.coordsTo3D())

		x,y,h = pcoords3D

		# On efface le cube du dico
		self.DICO[(prec_x,prec_y)].remove(pcube.h)
		if(self.DICO[(prec_x,prec_y)] == []): # si on a enleve le dernier de la liste, on enleve la cle
			del self.DICO[(prec_x,prec_y)]
		
		precoords = pcube.coords # coordonnees precedentes du cube

		coords_canvas = self.grille.grilleToCanvas((x - h, y - h)) # on veut les coordonnees "reelles", dans le canvas
		delta = (coords_canvas[0] - precoords[0], coords_canvas[1] - precoords[1])

		self.canv.move("cube_"+str(pcube.id), delta[0],delta[1])

		pcube.coords = coords_canvas
		pcube.h = h
		self.insererDansDisplayList(pcube)
		self.addCubeToDico(pcoords3D[:2],pcoords3D[2])

	def deplacerCube(self,event,plus_x = 0,plus_y = 0):
		''' Fonction pour deplacer un cube en fonction des fleches directionnelles, les parametres
			plus_x et plus_y indiquent ou sera placé le cube apres la fonction '''
		if(plus_y == 1):
			self.zone_dessin.itemconfig(self.fleche_haut,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_bas,fill = "red")
			self.zone_dessin.itemconfig(self.fleche_gauche,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_droite,fill = "black")
		elif(plus_y == -1):
			self.zone_dessin.itemconfig(self.fleche_haut,fill = "red")
			self.zone_dessin.itemconfig(self.fleche_bas,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_gauche,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_droite,fill = "black")
		elif(plus_x == 1):
			self.zone_dessin.itemconfig(self.fleche_haut,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_bas,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_gauche,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_droite,fill = "red")
		elif(plus_x == -1):
			self.zone_dessin.itemconfig(self.fleche_haut,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_bas,fill = "black")
			self.zone_dessin.itemconfig(self.fleche_gauche,fill = "red")
			self.zone_dessin.itemconfig(self.fleche_droite,fill = "black")
		
		x,y = self.grille.closestPoint(self.cube_select.coordsTo3D()) # x et y sont les positions 3D du cube, nous prenons alors en compte la hauteur
		h = self.cube_select.h

		x2,y2 = x+plus_x,y+plus_y # prochaine position du cube

		# On teste si il y a deja un cube dans la nouvelle position
		if((x2,y2) in self.DICO):
			# si oui, alors on deplace le cube au dessus du plus haut cube
			h = max(self.DICO[(x2,y2)])

			self.translationCube(self.cube_select,(x2,y2,h+1))
			
			self.pos_cube.set("position | x:"+str(int(x2))+" y:"+str(int(y2))+" hauteur: "+str(h+1))
		else:
			# sinon, on le deplace à la hauteur 0
			self.translationCube(self.cube_select,(x2,y2,0))
			
			self.pos_cube.set("position | x:"+str(int(x2))+" y:"+str(int(y2))+" hauteur: 0")

	def onCubeClick(self,event):
		''' Fonction pour la selection des cubes '''
		if(self.cube_select != None):
			self.cacherInfos()
			# On deselectionne le cube d'avant
			self.cube_select.deselectionCube()
			# On supprime les bindings des fleches directionnelles
			self.root.unbind("<Left>")
			self.root.unbind('<Right>')
			self.root.unbind('<Up>')
			self.root.unbind('<Down>')
			self.cube_select = None

		currentCoords = (event.x,event.y)
		convertedCoords = self.grille.canvasToGrille(currentCoords)
		faceCliquee = self.canv.find_withtag("current") # id du polygone sur lequel on a clique

		if(self.canv.type(faceCliquee) == "polygon"): # si on a bien clique sur un polygone (une face de cube)
			idCube = int(self.canv.gettags(faceCliquee)[0].split("_")[1]) # tag 0 : "cube_idfaceduhaut"
			cube = self.rechercherCube(idCube)
			if(cube != 0):
				self.montrerInfos()
				coords_cube_grille = self.grille.canvasToGrille(cube.coords)
				self.nom_cube.set("cube n°"+str(cube.numero))
				self.pos_cube.set("position | x:"+str(int(coords_cube_grille[0]+cube.h))+" y:"+str(int(coords_cube_grille[1]+cube.h))+" hauteur: "+str(cube.h))
				cube.selectionCube()
				self.cube_select = cube
				# On bind les fleches directionnelles a la fonction deplacerCube
				self.root.bind('<Left>', lambda event:self.deplacerCube(event,plus_x = -1))
				self.root.bind('<Right>', lambda event:self.deplacerCube(event,plus_x= 1))
				self.root.bind('<Up>', lambda event:self.deplacerCube(event,plus_y = -1))
				self.root.bind('<Down>', lambda event:self.deplacerCube(event,plus_y = 1))

	def annulerDernierCube(self,event=None):
		"""Annule le dernier placement de cube."""
		# le parametre event est obligatoire pour etre bind
		if len(self.CUBES) > 0:
			self.supprimerCube(self.CUBES[-1])

	def supprimerCube(self,pcube=None):
		# si c'est le dernier cube present
		if len(self.CUBES) == 1:
			self.deroulFichier.entryconfigure(2,state="disabled") # option Sauver
			self.deroulFichier.entryconfigure(3,state="disabled") # option Annuler
		# vu qu'on en passe un en parametre, on est sur qu'il y en a au moins un
		self.NB_CUBES -= 1 #Un cube en moins dans la scene
		self.canv.itemconfigure(self.texte_cubes, text="Nombre de cubes dans la scene: "+str(self.NB_CUBES))
		
		if not(pcube):
			pcube = self.cube_select
			self.cacherInfos() # On enleve le cube selectionne donc plus d'informations sur lui
		x,y = pcube.coordsTo3D()
		self.DICO[(x,y)].pop()
		if(self.DICO[(x,y)] == []):
			del self.DICO[(x,y)]
		pcube.effacer()
		self.CUBES.remove(pcube)

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

		self.NB_CUBES += 1 #Un cube en plus dans la scene
		self.canv.itemconfigure(self.texte_cubes, text="Nombre de cubes dans la scene: "+str(self.NB_CUBES))

		cube = Cube.Cube(self.canv,self.grille,coordsGrille,phauteur,pcouleur, self.NB_CUBES)
		self.insererDansDisplayList(cube)


		self.CUBES.append(cube)
		# on active les options d'exportation, de sauvegarde et d'annulation
		self.deroulFichier.entryconfigure(2,state="normal")
		self.deroulFichier.entryconfigure(3,state="normal")
		self.deroulFichier.entryconfigure(4,state="normal")
		return cube

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
		couleur_gauche_hexa_entry = tk.Entry(frame_couleur_gauche,width=10,justify=tk.CENTER,textvariable=self.__stringvar_couleur_gauche)
		couleur_droite_hexa_entry = tk.Entry(frame_couleur_droite,width=10,justify=tk.CENTER,textvariable=self.__stringvar_couleur_droite)

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

	# Mise a jour des Scales

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
		self.__cube_couleur.changerCouleur(nouvelle_couleur)
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

			# RVB
			self.__stringvar_couleur_haut.set(nouvelle_couleur[0])
			self.__stringvar_couleur_droite.set(nouvelle_couleur[2])

			# hexa
			self.__code_couleur_haut_RVB.set(int(nouvelle_couleur[0][1:],16))
			self.__code_couleur_droite_RVB.set(int(nouvelle_couleur[2][1:],16))

			# mise a jour des Entries des autres faces
			triplet_temp = self.hex2dec(nouvelle_couleur[0])
			for i in range(3):
				self.__couleur_haut_entry_RVB[i].delete(0,tk.END)
				self.__couleur_haut_entry_RVB[i].insert(tk.END,triplet_temp[i])
			triplet_temp = self.hex2dec(nouvelle_couleur[2])
			for i in range(3):
				self.__couleur_droite_entry_RVB[i].delete(0,tk.END)
				self.__couleur_droite_entry_RVB[i].insert(tk.END,triplet_temp[i])

		else:
			nouvelle_couleur[0] = self.__stringvar_couleur_haut.get()
			nouvelle_couleur[2] = self.__stringvar_couleur_droite.get()
		# on change la couleur du cube
		self.__cube_couleur.changerCouleur(nouvelle_couleur)
		# on modifie les entries
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
			
			# RVB
			self.__stringvar_couleur_haut.set(nouvelle_couleur[0])
			self.__stringvar_couleur_gauche.set(nouvelle_couleur[1])

			# hexa
			self.__code_couleur_haut_RVB.set(int(nouvelle_couleur[0][1:],16))
			self.__code_couleur_gauche_RVB.set(int(nouvelle_couleur[1][1:],16))

			# mise a jour des Entries des autres faces
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
		
		# on change la couleur du cube
		self.__cube_couleur.changerCouleur(nouvelle_couleur)
		# on modifie les entries
		for i in range(3):
			self.__couleur_droite_entry_RVB[i].delete(0,tk.END)
			self.__couleur_droite_entry_RVB[i].insert(tk.END,triplet_droite[i])


	# Gestion d'evenements

	def onMotion(self, event):
		if self.visualiser.get() == False:
			if self.cubeTest:
				self.cubeTest.effacer()
				self.cubeTest = None
			return
		d = self.grille.definition
		coordsEvent = (event.x,event.y)
		coordsGrille = self.grille.canvasToGrille(coordsEvent)

		if(self.cubeTest == None):
			# On cree le cube qui sera celui de la previsualisation
			if(self.grille.is_in_grille(coordsEvent)):
				self.cubeTest = Cube.Cube(self.canv,self.grille,coordsGrille,0,pcouleur=("#f2e6e3","#f2e6e3","#f2e6e3")) # On place le cube si l'utilisateur entre dans la grille
				self.cubeTest.desactiver() # on met et disable le cube pour qu'on ne puisse par cliquer dessus
				self.precoords = coordsEvent
		else:
			currentFace = self.canv.find_withtag("current") # id du polygone sur lequel on est
			new_coords = self.grille.grilleToCanvas(self.grille.closestPointUp(self.grille.canvasToGrille(coordsEvent)))
			# (note par mathieu : je pense qu'il faudrait creer une fonction pour avoir les new_coords plus joliment)
			if(self.canv.type(currentFace) == "polygon"): # si on a est bien sur un polygone (une face de cube)
				idCube = int(self.canv.gettags(currentFace)[0].split("_")[1]) # tag 0 : "cube_idfaceduhaut"
				cube = self.rechercherCube(idCube)
				if(cube != 0):
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
			cube = self.rechercherCube(idCube)
			if(cube != 0):
				x,y = self.grille.canvasToGrille(cube.coords) # coordonnees 2D "reelles" du cube dans la grille

				position3D = (x+cube.h,y+cube.h,cube.h) # on obtient les coordonnees de hauteur 0 (case de base), et la hauteur

				# on teste les id de faces pour savoir laquelle c'etait ; faceCliquee[0] car c'est un tuple
				if faceCliquee[0] == cube.haut:
					self.placerCubeHaut(position3D)
				elif faceCliquee[0] == cube.gauche:
					self.placerCubeGauche(position3D)
				elif faceCliquee[0] == cube.droite:
					self.placerCubeDroite(position3D)

		elif self.grille.is_in_grille(currentCoords):
			# sinon ce n'est pas un polygone alors on a clique autre part : on regarde si c'est dans la grille
			# il faut supprimer la limite de placement en vertical vers le haut, sinon on peut pas faire + de 1 cube en (0,0)
			hauteur = 0
			self.placerCube(self.grille.closestPointUp(convertedCoords),hauteur) # on ajuste le point 0.5 case plus haut
		if(self.cubeTest):
			self.cubeTest.priorite() # a changer par inserer

	def quitter(self):
		self.root.quit()

	def montrerInfos(self):
		# Pour rendre les infos visibles
		self.info_nom.pack()
		self.info_pos.pack()
		self.zone_dessin.pack()
		self.supprimer_bouton.pack()

	def cacherInfos(self):
		# Pack forget pour ne plus rendre les infos visibles
		self.info_nom.pack_forget()
		self.info_pos.pack_forget()
		self.zone_dessin.pack_forget()
		self.supprimer_bouton.pack_forget()

	def initInfos(self):
		# Affichage des informations
		self.nom_cube = tk.StringVar()
		self.pos_cube = tk.StringVar()
		self.zone_dessin = tk.Canvas(self.fenetre,width=100,height=50,bd=8)
		self.fleche_haut = self.zone_dessin.create_line(60,30,60,15,fill="black",width=10, arrow="last")
		self.fleche_bas = self.zone_dessin.create_line(60,60,60,45,fill="black",width=10, arrow="first")
		self.fleche_gauche = self.zone_dessin.create_line(60,38,30,38,fill="black",width=10, arrow="last")
		self.fleche_droite = self.zone_dessin.create_line(60,38,90,38,fill="black",width=10, arrow="last")
		self.zone_dessin.pack()

		self.info_nom = tk.Label(self.fenetre, textvariable=self.nom_cube)
		self.info_pos = tk.Label(self.fenetre, textvariable=self.pos_cube)
		self.info_nom.pack()
		self.info_pos.pack()

		self.supprimer_bouton = tk.Button(self.fenetre,text="Supprimer ce cube",command=self.supprimerCube)
		self.supprimer_bouton.pack()

		self.fenetre.pack(fill="both", expand="yes",side="left")

	def apropos(self):
		# Ouverture d'une nouvelle fenetre

		# On prend les infos de la root window, pour positionner la fentre en haut a gauche de la root
		x = self.root.winfo_x()
		y = self.root.winfo_y()

		fenetre = tk.Toplevel(self.root)
		fenetre.resizable(width=False, height=False)
		fenetre.title("A propos")
		fenetre.geometry("+%d+%d" % (x,y))
		tk.Label(fenetre, text="Projet IHM L3 informatique").pack()
		tk.Label(fenetre, text="Copyright © 2020-2021").pack()
		label_dev = tk.LabelFrame(fenetre, text="Développeurs")
		tk.Label(label_dev, text="RESSEGUIER Mathieu et BOGADO GARCIA Maximino").pack()
		label_dev.pack()
		fenetre.grab_set()
		self.root.wait_window(fenetre)

	def ouvrirDocumentation(self):
		webbrowser.open('doc.html')

	# Constructeur de l'application

	def __init__(self):

		# Root
		self.root = tk.Tk()

		# LabelFrame qui contiendra les informations d'un cube lorsqu'on clique dessus
		self.fenetre = tk.LabelFrame(self.root, text="Infos", padx=20, pady=20)
		self.initInfos()
		self.cacherInfos()

		# Menus

		self.menuFrame = tk.Frame(self.root)
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
		self.visualiser = tk.BooleanVar(value=True)
		self.deroulFichier.add_checkbutton(label="Visualiser", variable=self.visualiser)
		self.deroulFichier.add_command(label="Couleur", command=self.ouvrirFenetreCouleur)
		self.deroulFichier.add_separator()
		self.deroulFichier.add_command(label="Quitter", command=self.quitter)

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
		self.deroulAide = tk.Menu(self.menuAide,tearoff=False)
		self.deroulAide.add_command(label="Documentation", command=self.ouvrirDocumentation)
		self.deroulAide.add_command(label="A propos", command=self.apropos)
		self.menuAide.config(menu=self.deroulAide)
		self.menuAide.pack(side=tk.RIGHT)

		# Canvas

		self.canv = tk.Canvas(self.root,width=500,height=500,bg="white")
		self.texte_cubes = self.canv.create_text(390,480,fill="black",text="Nombre de cubes dans la scene: "+str(self.NB_CUBES))
		self.canv.bind("<Motion>",self.onMotion)
		self.canv.bind("<Button-1>",self.onClick)
		self.canv.bind("<Button-3>",self.onCubeClick)

		self.grille = Grille.Grille(self.canv)
		self.cubeTest = None
		# cube1 = Cube.Cube(self.canv,self.grille,(1,1))

		self.canv.pack()

		# Fin

		self.root.mainloop()


App()

exit(0)
