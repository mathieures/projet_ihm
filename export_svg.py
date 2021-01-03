from tkinter import filedialog,messagebox

def sauver_svg(pcanvas,pgrille,pliste_cubes,pcube_visu):
	"""
	Appelee en premier, cette fonction ouvre un fichier SVG et dessine le projet actuel.
	"""
	global grille
	grille = pgrille

	fichier = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=(("SVG files", ".svg"),("All files", ".*")))
	# try:
	with open(fichier, "w", encoding = "utf-8") as f:
		# Ecriture du header xml, puis d'une viewbox, qui est en realite comme notre canvas
		f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
		f.write("<svg viewBox=" + "\"0 0 " + str(pcanvas.cget("width")) + " " + str(pcanvas.cget("height")) + "\" " + "xmlns=\"http://www.w3.org/2000/svg\">\n")
		_dessiner_grille_svg(f)
		# pas optimise, mais facultatif
		liste = pcanvas.find_all()[grille.taille_x+grille.taille_y+3:] # a partir du nb de lignes+1 jusqu'a la fin : les faces des cubes
		# attention : les id commencent a 1
		for i in range(0,len(liste),3):
			if liste[i] != pcube_visu.id: # verifier si ça fonctionne toujours avec les pixmaps (autres types de polygones peut-etre ?)
				# on a un id de cube, il nous faut l'objet pour avoir ses coordonnees
				for c in pliste_cubes:
					if c.id == liste[i]:
						cube = c
						break
				# cube est le cube correspondant a l'id i
				coords2D = grille.canvas_to_grille(cube.coords)
				_dessiner_cube_svg(coords2D,f,cube.h,cube.couleur)
		f.write("</svg>")
	# except: # Si il y a une erreur, le dire a l'utilisateur, (gerer les differentes erreurs apres !!!!)
	# 	messagebox.showerror(title="Error", message="Erreur lors de l'ouverture du fichier.")
	# 	# attention : appele aussi quand l'utilisateur clique sur Annuler

def _dessiner_grille_svg(pfichier):
	"""Cette fonction dessine la grille dans un fichier SVG grace a des balises <line>"""
	global grille
	if not(grille):
		return
	x = grille.origine[0]
	y = grille.origine[1]
	d = grille.definition
	taille_x = grille.taille_x
	taille_y = grille.taille_y
	# c'est en realite la meme methode que dans grille.dessinegrille()
	for i in range(taille_y+1):
		pfichier.write("<line x1=\"" + str(x) + "\" " + "x2=\"" + str(x+d*taille_y) + "\" " + "y1=\"" + str(y) + "\" " + "y2=\"" + str(y+(d*taille_y/2)) + "\"")
		x -= d
		y += d/2
		pfichier.write(" stroke=\"grey\"")
		pfichier.write("/>\n")
	x = grille.origine[0]
	y = grille.origine[1]
	for j in range(taille_x+1):
		pfichier.write("<line x1=\"" + str(x) + "\" " + "x2=\"" + str(x-d*taille_y) + "\" " + "y1=\"" + str(y) + "\" " + "y2=\"" + str(y+(d*taille_y/2)) + "\"")
		x += d
		y += d/2
		pfichier.write(" stroke=\"grey\"")
		pfichier.write("/>\n")

def _dessiner_cube_svg(pcoords_grille,pfichier,phauteur,pcouleur):
	"""Fonction qui dessine un cube dans un fichier SVGgrace a des balises <polygon>"""
	global grille
	if not(grille):
		return
	d = grille.definition
	canv_coords = grille.grille_to_canvas(pcoords_grille)
	x = canv_coords[0]
	y = canv_coords[1]
	# c'est en realite la meme methode que dans cube.dessiner()
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