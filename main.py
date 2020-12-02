import tkinter as tk
import Grille
import Cube

CUBES = [] # liste des cubes places

def nouveauFichier():
	global CUBES
	# on efface tous les cubes
	for cube in CUBES:
		cube.effacer(canv)
	# canv.delete("tag_cube") # plus simple a ecrirre qu'appeler Cube.effacer() pour tous les cubes
	CUBES = []
	# on desactive l'option de sauvegarde
	# deroulFichier.entryconfigure(2,state="disabled")

def annulerDernierCube():
	global CUBES
	if len(CUBES) > 0:
		CUBES[-1].effacer(canv)
		CUBES.pop()
	else:
		print("plus de cubes dans la liste")
		#on desactive l'option pour annuler
		deroulFichier.entryconfigure(1,state="disabled")

def placerCube(pcoordsGrille):
	global CUBES
	"""Prend en parametre des coordonnes de grille (peut-etre a changer ?)"""
	print("		placed cube at :",grille.closestPoint(pcoordsGrille))
	cube = Cube.Cube(canv,grille,grille.closestPoint(pcoordsGrille),ptags="tag_cube")
	CUBES.append(cube)
	return cube


def onClick(event):
    currentCoords = (event.x,event.y)
    convertedCoords = grille.canvasToGrille((currentCoords))
    print("click on :",currentCoords,"=>",convertedCoords)
    placerCube(convertedCoords)

# Root

root = tk.Tk()
# root.geometry("300x300")


# Menus

menuFrame = tk.Frame(root,bg="red")
menuFrame.pack(side=tk.TOP,expand=True,fill=tk.X,anchor="n")

bottomFrame = tk.Frame(root,bg="blue")
bottomFrame.pack(side=tk.BOTTOM,expand=True,fill=tk.X,anchor="s")

# Menu fichier

menuFichier = tk.Menubutton(menuFrame,text="Fichier",underline=0,relief="raised")

deroulFichier = tk.Menu(menuFichier, tearoff=False)
deroulFichier.add_command(label="Nouveau", command=nouveauFichier)
deroulFichier.add_command(label="Annuler", command=annulerDernierCube)

deroulFichier.entryconfigure(1,state="disabled")

# deroulFichier.add_command(label="Ouvrir", command=openFile)
# deroulFichier.add_command(label="Sauver", command=saveFile)
# deroulFichier.add_command(label="Quitter", command=quitApp)
# root.protocol("WM_DELETE_WINDOW", quitApp) # pour gerer la fermeture avec la croix rouge et alt-f4

# # on desactive l'option de sauvegarde (il faudrait trouver par nom plutot)
# deroulFichier.entryconfigure(2,state="disabled")

menuFichier.config(menu=deroulFichier)
menuFichier.pack(side=tk.LEFT)

# Menu aide

menuAide = tk.Menubutton(menuFrame,text="Aide",underline=0,relief="raised")

derouleAide = tk.Menu(menuAide,tearoff=False)

menuAide.config(menu=derouleAide)
menuAide.pack(side=tk.RIGHT)

# Canvas

canv = tk.Canvas(root,width=500,height=500,bg="white")
canv.bind("<Button-1>",onClick)

grille = Grille.Grille(canv)

# cube1 = Cube.Cube(canv,grille,(1,1))


canv.pack()
# print("is ready :",isReadyToDraw)


# Fin

root.mainloop()

exit(0)
