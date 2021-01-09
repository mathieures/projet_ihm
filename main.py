import tkinter as tk
import grille
import cube
import dico
import codes_couleur
import export_svg
from tkinter import filedialog, messagebox

 # Pour la documentation
import webbrowser
import os

class App:

    # Valeurs par defaut

    __couleur_cube = [
        "#afafaf",
        "#808080",
        "#414141"
    ] # couleur des cubes par defaut
    __COULEUR_MAX = 16777215 # la couleur #ffffff en decimal (constante)

    __cube_visu = None
    __cube_select = None
    NB_CUBES = 0 # Pour savoir combien il y a de cubes dans la scene, et pour leur attribuer des numeros
    __precoords = () # Tuple pour memoriser les coordonnees precedentes pour le previsualisation

    DICO = dico.Dico() # contient la position 3D de tous les cubes
    #                    sous la forme dico[(x, y)] = [hauteur_1, hauteur_2...]

    CUBES = [] # liste des cubes presents dans la scene


    # Fonctions d'interaction avec tkinter
    
    def inserer_dans_display_list(self, pcube):
        """
        Permet d'inserer un cube dans la display list
        a la bonne position, avec la bonne perspective
        """
        coords3D = pcube.coords_to_3D()
        # index de la face du haut dans la liste de tous les elements du canvas
        index_cube = self.canv.find_all().index(pcube.id)

        # le tag "cube_idfaceduhaut", qu'ont toutes les faces du cube
        tag = "cube_"+str(pcube.id)
        for autre_cube in self.CUBES:
            if autre_cube == pcube:
                continue
            
            display_list = self.canv.find_all()

            # index de la face du haut dans la liste de tous les elements du canvas
            index_cube = display_list.index(pcube.id)
            autre_index = display_list.index(autre_cube.id)

            autre_coords3D = autre_cube.coords_to_3D()

            if (pcube.h > autre_cube.h and autre_index > index_cube):
                # si le nouveau cube est plus haut mais dessine plus bas que l'autre
                self.canv.tag_raise(tag,(autre_cube.id+2))
                # +2 : on doit placer le cube au dessus de toute face de autre_cube
            elif (pcube.h < autre_cube.h and autre_index < index_cube):
                self.canv.tag_lower(tag, autre_cube.id) # le nouveau est plus bas
            elif pcube.h == autre_cube.h:
                # a chaque condition si elle est fausse le cube est deja bien place
                if coords3D[0] >= autre_coords3D[0]:
                    if (coords3D[1] >= autre_coords3D[1] and
                        autre_index > index_cube):
                        self.canv.tag_raise(tag,(autre_cube.id+2))
                    elif (coords3D[1] < autre_coords3D[1] and
                          autre_index < index_cube):
                        self.canv.tag_lower(tag, autre_cube.id)
                elif coords3D[0] < autre_coords3D[0]:
                    if (coords3D[1] > autre_coords3D[1] and
                        autre_index > index_cube):
                        self.canv.tag_raise(tag,(autre_cube.id+2))
                    elif (coords3D[1] <= autre_coords3D[1] and
                          autre_index < index_cube):
                        self.canv.tag_lower(tag, autre_cube.id)

    def toggle_visu(self,event):
        """
        Active/desactive la visualisation en fonction de sa valeur courante.
        Utile pour bind Ctrl + V a la variable.
        """
        self.__visualiser.set(not self.__visualiser.get())




    # Manipulation de fichiers (hors d'un module a cause des multiples bindings)
    
    def nouveau_fichier(self, event=None):
        self.NB_CUBES = 0
        self.canv.itemconfigure(
            self.texte_nb_cubes,
            text="Nombre de cubes dans la scene : " + str(self.NB_CUBES)
        )
        # on efface tous les cubes
        for cube in self.CUBES:
            cube.effacer()

        self.CUBES = []
        self.DICO.vider()
        # On desactive les options Sauver, Exporter et Annuler
        self.deroul_fichier.entryconfigure(2, state="disabled")
        self.deroul_fichier.entryconfigure(3, state="disabled")
        self.deroul_edition.entryconfigure(2, state="disabled")

    def sauver_fichier(self, event=None):
        # On demande a l'utilisateur dans quel fichier il veut sauver le projet
        fichier = filedialog.asksaveasfilename(
            defaultextension=".ihm",
            filetypes=(("Text files", ".ihm"),("All files", ".*"))
        )
        if not fichier:
            return # l'utilisateur a annule ou ferme la fenetre
        try: # On ecrit dans le fichier les coordonnees et couleurs des cubes
            f = open(fichier, "w", encoding = "utf-8")
        except FileNotFoundError:
            messagebox.showerror(
                title="Error",
                message="Erreur fichier non trouvé"
            )
        except IOError:
            messagebox.showerror(
                title="Error",
                message="Le fichier n'existe pas"
            )
        else:
            for cube in self.CUBES:
                coords3D = cube.coords_to_3D()
                couleur_faces = cube.couleur
                f.write(f"{coords3D[0]},{coords3D[1]},{cube.h},"
                      + f"{couleur_faces[0]},{couleur_faces[1]},{couleur_faces[2]}\n")
            f.close()

    def ouvrir_fichier(self, event=None):
        ext=''
        fichier = filedialog.askopenfile(
            mode="r", defaultextension=".ihm",
            filetypes=(("Fichiers IHM", ".ihm"),("All files", ".*")))
        if fichier:
            self.nouveau_fichier()
            for ligne in fichier.readlines():
                parse = ligne.rstrip().split(',')
                self.placer_cube(
                    (int(parse[0]), int(parse[1])),
                     int(parse[2]), parse[3:6]
                )
            fichier.close()


    # Export en SVG (utilisation du module dedie)
    def sauver_svg(self, event=None):
        export_svg.sauver_svg(self.canv, self.grille, self.CUBES, self.__cube_visu)


    # Manipulation des cubes

    def placer_cube(self, pcoords_grille, phauteur, pcouleur=None):
        """
        Place un cube grace a des coordonnees de grille.
        Note : replace la position au point le plus proche.
        """
        # coordonnees de la case ou est place le cube
        coords3D = self.grille.closest_point(pcoords_grille)
        self.DICO[coords3D] = phauteur

        # on transforme les coordonnees 3D en coordonnees 2D "aplaties",
        #  transposees "comme on les voit", sans hauteur
        coords_grille = (coords3D[0]-phauteur, coords3D[1]-phauteur)
        if pcouleur is None:
            pcouleur = self.__couleur_cube

        self.NB_CUBES += 1 #Un cube en plus dans la scene
        self.canv.itemconfigure(
            self.texte_nb_cubes,
            text="Nombre de cubes dans la scene : " + str(self.NB_CUBES))

        cube_tmp = cube.Cube(
            self.canv, self.grille, coords_grille,
            phauteur, pcouleur, self.NB_CUBES)
        self.inserer_dans_display_list(cube_tmp)


        self.CUBES.append(cube_tmp)
        # on active les options d'exportation, de sauvegarde et d'annulation
        self.deroul_fichier.entryconfigure(2, state="normal")
        self.deroul_fichier.entryconfigure(3, state="normal")
        self.deroul_edition.entryconfigure(2, state="normal")

    def placer_cube_haut(self, pposition3D):
        """
        Place un cube en haut de la position 3D passee en parametre.
        pposition3D de la forme (x, y, hauteur).
        """
        x, y, h = pposition3D
        return self.placer_cube((x, y), h+1)

    def placer_cube_gauche(self, pposition3D):
        """Place un cube a gauche de la position 3D"""
        x, y, h = pposition3D
        return self.placer_cube((x, y+1), h)

    def placer_cube_droite(self, pposition3D):
        """Place un cube a droite de la position 3D"""
        x, y, h = pposition3D
        return self.placer_cube((x+1, y), h)


    def translation_cube(self, pcube, pcoords3D):
        """
        Deplace un cube a la position (tuple de longueur 3)
        passee en parametre, inconditionnellement.
        """
        prec_grille = self.grille.closest_point(pcube.coords_to_3D())

        # On efface le cube du dico
        self.DICO.enlever((prec_grille[0], prec_grille[1]), pcube.h)

        x, y, h = pcoords3D
        
        prec_canvas = pcube.coords # coordonnees precedentes du cube

        # on veut les coordonnees dans le canvas des nouvelles coordonnees
        coords_canvas = self.grille.grille_to_canvas((x - h, y - h))
        delta = (coords_canvas[0] - prec_canvas[0],
                 coords_canvas[1] - prec_canvas[1])

        self.canv.move("cube_"+str(pcube.id), delta[0], delta[1])

        pcube.coords = coords_canvas
        pcube.h = h
        self.inserer_dans_display_list(pcube)
        self.DICO[(x, y)] = h

    def deplacer_cube(self, event, plus_x = 0, plus_y = 0):
        """
        Fonction pour deplacer un cube en fonction des fleches directionnelles.
        Les parametres indiquent ou sera placé le cube.
        """
        if plus_y == 1:
            self.zone_dessin.itemconfig(self.fleche_haut, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_bas, fill = "red")
            self.zone_dessin.itemconfig(self.fleche_gauche, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_droite, fill = "black")
        elif plus_y == -1:
            self.zone_dessin.itemconfig(self.fleche_haut, fill = "red")
            self.zone_dessin.itemconfig(self.fleche_bas, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_gauche, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_droite, fill = "black")
        elif plus_x == 1:
            self.zone_dessin.itemconfig(self.fleche_haut, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_bas, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_gauche, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_droite, fill = "red")
        elif plus_x == -1:
            self.zone_dessin.itemconfig(self.fleche_haut, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_bas, fill = "black")
            self.zone_dessin.itemconfig(self.fleche_gauche, fill = "red")
            self.zone_dessin.itemconfig(self.fleche_droite, fill = "black")
        
        x, y = self.__cube_select.coords_to_3D() # case "de base" du cube
        h = self.__cube_select.h

        x2, y2 = x+plus_x, y+plus_y # prochaine position du cube

        # On teste si il y a deja un cube dans la nouvelle position
        if (x2, y2) in self.DICO:
            # si oui, alors on deplace le cube dans le premier vide
            hauteurs = self.DICO[(x2, y2)]
            for i in range(max(hauteurs)+2):
                # +1 car on veut avoir aussi la plus grande valeur
                #  et +1 pour avoir max+1 si on arrive au bout
                if i not in hauteurs:
                    h = i # h est la premiere hauteur non-presente
                    break

            self.translation_cube(self.__cube_select,(x2, y2, h))
            self.pos_cube.set("position |"
                + " x : " + str(int(x2))
                + " y : " + str(int(y2))
                + " hauteur : " + str(h))
        else:
            # sinon, on le deplace à la hauteur 0
            self.translation_cube(self.__cube_select,(x2, y2, 0))
            self.pos_cube.set("position | "
                + " x : " + str(int(x2))
                + " y : " + str(int(y2))
                + " hauteur : 0")


    def supprimer_cube(self, event=None, pcube=None):
        """
        Supprime le cube passe en parametre.
        Si aucun n'est specifie, tente de supprimer celui selectionne.
        """
        # On supprime les bindings des fleches directionnelles pour eviter un key error du Dico
        self.root.unbind("<Left>")
        self.root.unbind('<Right>')
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        # vu qu'on en passe un en parametre, on est sur qu'il y en a au moins un
        self.NB_CUBES -= 1 #Un cube en moins dans la scene
        self.canv.itemconfigure(
            self.texte_nb_cubes,
            text="Nombre de cubes dans la scene : " + str(self.NB_CUBES)
        )
        
        if pcube is None:
            # si on ne precise aucun cube (notamment a cause du bind)
            # on supprime le cube selectionne
            if self.__cube_select is not None:
                pcube = self.__cube_select
                self.cacher_infos() # Plus de selection donc plus d'informations
            else:
                return
        x, y = pcube.coords_to_3D()
        self.DICO.enlever((x, y), pcube.h)

        pcube.effacer()
        self.CUBES.remove(pcube)
        
        # si la liste est vide apres la suppression
        if not self.CUBES:
            # on desactive l'option Annuler
            self.deroul_edition.entryconfigure(2, state="disabled")

    def annuler_dernier_cube(self, event=None):
        """Annule le dernier placement de cube."""
        # le parametre event est obligatoire pour etre bind
        if len(self.CUBES) > 0:
            self.supprimer_cube(pcube=self.CUBES[-1])


    def rechercher_cube(self, pid):
        """
        A partir d'un id, la fonction renvoie
        l'objet cube correspondant a cet id.
        """
        for cube in self.CUBES: # on teste chaque cube deja place
            if cube.id == pid: # si c'est que l'on cherche on le renvoie
                return cube
        return None


    # Selection de couleur

    def ouvrir_fenetre_couleur(self,event=None):
        """
        Ouvre la fenetre de selection des couleurs pour les cubes.
        Impossible a modulariser, car intervient sur __couleur_cube
        (il faudrait donc importer ce fichier, causant une dependance circulaire)
        """
        self.__fenetre_couleur = tk.Toplevel(self.root)
        
        # Visualisation du cube a gauche
        self.__canvas_couleur = tk.Canvas(
            self.__fenetre_couleur,
            width=160, height=100)
        self.__canvas_couleur.pack(side=tk.LEFT)

        grille_couleur = grille.Grille(
            self.__canvas_couleur, 25, 1, 1,
            porigine=(80, 50)) # d = 10, taille_x, taille_y = 1, 1
        self.__cube_couleur = cube.Cube(
            self.__canvas_couleur, grille_couleur, (0, 0),
            phauteur=0, pcouleur=self.__couleur_cube)

        # Initialisation des Frames
        frame_couleur_right = tk.Frame(self.__fenetre_couleur)
        frame_couleur_right.pack(side=tk.TOP)
        frame_couleur_RVB = tk.Frame(frame_couleur_right)
        frame_couleur_RVB.pack(side=tk.TOP, anchor="nw")

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
        self.__str_couleur_haut = tk.StringVar(value=self.__couleur_cube[0])
        self.__str_couleur_gauche = tk.StringVar(value=self.__couleur_cube[1])
        self.__str_couleur_droite = tk.StringVar(value=self.__couleur_cube[2])

        # Valeurs decimales, calculees grace aux codes hexa
        self.__code_haut_RVB = tk.IntVar(value=int(self.__couleur_cube[0][1:],16))
        self.__code_gauche_RVB = tk.IntVar(value=int(self.__couleur_cube[1][1:],16))
        self.__code_droite_RVB = tk.IntVar(value=int(self.__couleur_cube[2][1:],16))

        # Affichage des codes dans des Entries
        label_couleur_texte = tk.Label(frame_couleur_RVB, text="  R :     V :     B :    code hex :")
        label_couleur_texte.pack()
        
        triplets = [codes_couleur.calculer_triplet(self.__code_haut_RVB.get()),
                    codes_couleur.calculer_triplet(self.__code_gauche_RVB.get()),
                    codes_couleur.calculer_triplet(self.__code_droite_RVB.get())]

        couleur_haut_entry_R = tk.Entry(
            frame_couleur_haut, width=4,
            justify=tk.CENTER)
        couleur_haut_entry_V = tk.Entry(
            frame_couleur_haut, width=4,
            justify=tk.CENTER)
        couleur_haut_entry_B = tk.Entry(
            frame_couleur_haut, width=4,
            justify=tk.CENTER)

        self.__entry_RVB_haut = [
            couleur_haut_entry_R,
            couleur_haut_entry_V,
            couleur_haut_entry_B
        ]

        for i in range(3):
            self.__entry_RVB_haut[i].insert(tk.END, str(triplets[0][i]))
            self.__entry_RVB_haut[i].pack(side=tk.LEFT)
            self.__entry_RVB_haut[i].config(state='readonly')

        couleur_gauche_entry_R = tk.Entry(
            frame_couleur_gauche, width=4,
            justify=tk.CENTER)
        couleur_gauche_entry_V = tk.Entry(
            frame_couleur_gauche, width=4,
            justify=tk.CENTER)
        couleur_gauche_entry_B = tk.Entry(
            frame_couleur_gauche, width=4,
            justify=tk.CENTER)

        self.__entry_RVB_gauche = [
            couleur_gauche_entry_R,
            couleur_gauche_entry_V,
            couleur_gauche_entry_B
        ]

        for i in range(3):
            self.__entry_RVB_gauche[i].insert(tk.END, str(triplets[1][i]))
            self.__entry_RVB_gauche[i].pack(side=tk.LEFT)
            self.__entry_RVB_gauche[i].config(state='readonly')

        couleur_droite_entry_R = tk.Entry(
            frame_couleur_droite, width=4,
            justify=tk.CENTER)
        couleur_droite_entry_V = tk.Entry(
            frame_couleur_droite, width=4,
            justify=tk.CENTER)
        couleur_droite_entry_B = tk.Entry(
            frame_couleur_droite, width=4,
            justify=tk.CENTER)

        self.__entry_RVB_droite = [
            couleur_droite_entry_R,
            couleur_droite_entry_V,
            couleur_droite_entry_B
        ]

        for i in range(3):
            self.__entry_RVB_droite[i].insert(tk.END, str(triplets[2][i]))
            self.__entry_RVB_droite[i].pack(side=tk.LEFT)
            self.__entry_RVB_droite[i].config(state='readonly')

        couleur_haut_hexa_entry = tk.Entry(
            frame_couleur_haut, width=10, justify=tk.CENTER,
            textvariable=self.__str_couleur_haut, state="readonly")
        couleur_gauche_hexa_entry = tk.Entry(
            frame_couleur_gauche, width=10, justify=tk.CENTER,
            textvariable=self.__str_couleur_gauche, state="readonly")
        couleur_droite_hexa_entry = tk.Entry(
            frame_couleur_droite, width=10, justify=tk.CENTER,
            textvariable=self.__str_couleur_droite, state="readonly")

        for entry in (couleur_haut_hexa_entry,
                      couleur_gauche_hexa_entry,
                      couleur_droite_hexa_entry):
            entry.pack(side=tk.LEFT)

        # Sliders affiches en bas
        # Note : modifier une variable liee n'appelle pas le callback,
        #  utile pour modifier toutes les scales en meme temps
        #  (https://stackoverflow.com/questions/4038517/tkinter-set-a-scale-value-without-triggering-callback)
        scale_couleur_haut = tk.Scale(
            bottom_frame_couleur, orient="horizontal", from_=0,
            to=self.__COULEUR_MAX, command=self.update_couleur_haut,
            showvalue=0, resolution=1, length=200,
            variable=self.__code_haut_RVB).pack()
        scale_couleur_gauche = tk.Scale(
            bottom_frame_couleur, orient="horizontal", from_=0,
            to=self.__COULEUR_MAX, command=self.update_couleur_gauche,
            showvalue=0, resolution=1, length=200,
            variable=self.__code_gauche_RVB).pack()
        scale_couleur_droite = tk.Scale(
            bottom_frame_couleur, orient="horizontal", from_=0,
            to=self.__COULEUR_MAX, command=self.update_couleur_droite,
            showvalue=0, resolution=1, length=200,
            variable=self.__code_droite_RVB).pack()


        # Mode alternatif : definit le comportement des sliders :
        #  modifiés ensemble (True) ou separement
        self.__mode_ensemble = tk.BooleanVar(value=True)
        couleur_check_mode_auto = tk.Checkbutton(
            bottom_frame_couleur,
            text="Modifier ensemble",
            variable=self.__mode_ensemble)
        couleur_check_mode_auto.pack(side=tk.LEFT)

        # Confirmer
        couleur_bouton_ok = tk.Button(
            bottom_frame_couleur,
            text="Ok", command=self.confirmer_couleur)
        couleur_bouton_ok.pack(side=tk.RIGHT, padx=10)

    # Mise a jour des Scales (grace aux IntVar)

    def update_couleur_haut(self, valeur):
        """
        On modifie les variables self.__couleur_* pour qu'elles correspondent
        aux valeurs des sliders de selection de couleur.
        On met aussi a jour la couleur des faces du cube.
        """
        val = int(valeur)
        triplet_haut = codes_couleur.calculer_triplet(val)
        code = codes_couleur.dec2hex(triplet_haut)
        
        self.__str_couleur_haut.set(code)
        
        nouvelle_couleur = [code, None, None]
        
        # si le mode ensemble est actif, on modifie les autres faces
        # note : les couleurs automatiques ne sont pas parfaites,
        #  mais dans certains cas fonctionnent plutot bien
        if self.__mode_ensemble.get():
            nouvelle_couleur[1] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(0.73142*val)))
            nouvelle_couleur[2] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(0.37142*val)))

            # codes RVB
            self.__str_couleur_gauche.set(nouvelle_couleur[1])
            self.__str_couleur_droite.set(nouvelle_couleur[2])
            
            # codes hexa
            self.__code_gauche_RVB.set(int(nouvelle_couleur[1][1:], 16))
            self.__code_droite_RVB.set(int(nouvelle_couleur[2][1:], 16))

            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[1])
            # on modifie chaque entry pour la face en fonction du code hexa
            for i in range(3):
                self.__entry_RVB_gauche[i].config(state="normal")
                self.__entry_RVB_gauche[i].delete(0, tk.END)
                self.__entry_RVB_gauche[i].insert(tk.END, triplet_temp[i])
                self.__entry_RVB_gauche[i].config(state="readonly")
            
            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[2])
            for i in range(3):
                self.__entry_RVB_droite[i].config(state="normal")
                self.__entry_RVB_droite[i].delete(0, tk.END)
                self.__entry_RVB_droite[i].insert(tk.END, triplet_temp[i])
                self.__entry_RVB_droite[i].config(state="readonly")

        else:
            nouvelle_couleur[1] = self.__str_couleur_gauche.get()
            nouvelle_couleur[2] = self.__str_couleur_droite.get()
        
        # dans tous les cas, on change la couleur du cube
        self.__cube_couleur.changer_couleur(nouvelle_couleur)
        # pour chaque face on modifie l'entry en fonction du code hexa
        for i in range(3):
            self.__entry_RVB_haut[i].config(state="normal")
            self.__entry_RVB_haut[i].delete(0, tk.END)
            self.__entry_RVB_haut[i].insert(tk.END, triplet_haut[i])
            self.__entry_RVB_haut[i].config(state="readonly")

    def update_couleur_gauche(self, valeur):
        val = int(valeur)
        triplet_gauche = codes_couleur.calculer_triplet(val)
        code = codes_couleur.dec2hex(triplet_gauche)

        self.__str_couleur_gauche.set(code)

        nouvelle_couleur = [None, code, None]
        
        if self.__mode_ensemble.get():
            nouvelle_couleur[0] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(2.6923*val)))
            nouvelle_couleur[2] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(1.9692*val)))

            # RVB
            self.__str_couleur_haut.set(nouvelle_couleur[0])
            self.__str_couleur_droite.set(nouvelle_couleur[2])

            # hexa
            self.__code_haut_RVB.set(int(nouvelle_couleur[0][1:], 16))
            self.__code_droite_RVB.set(int(nouvelle_couleur[2][1:], 16))

            # mise a jour des Entries des autres faces
            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[0])
            for i in range(3):
                self.__entry_RVB_haut[i].config(state="normal")
                self.__entry_RVB_haut[i].delete(0, tk.END)
                self.__entry_RVB_haut[i].insert(tk.END, triplet_temp[i])
                self.__entry_RVB_haut[i].config(state="readonly")
            
            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[2])
            for i in range(3):
                self.__entry_RVB_droite[i].config(state="normal")
                self.__entry_RVB_droite[i].delete(0, tk.END)
                self.__entry_RVB_droite[i].insert(tk.END, triplet_temp[i])
                self.__entry_RVB_droite[i].config(state="readonly")

        else:
            nouvelle_couleur[0] = self.__str_couleur_haut.get()
            nouvelle_couleur[2] = self.__str_couleur_droite.get()
        # on change la couleur du cube
        self.__cube_couleur.changer_couleur(nouvelle_couleur)
        # on modifie les entries
        for i in range(3):
            self.__entry_RVB_gauche[i].config(state="normal")
            self.__entry_RVB_gauche[i].delete(0, tk.END)
            self.__entry_RVB_gauche[i].insert(tk.END, triplet_gauche[i])
            self.__entry_RVB_gauche[i].config(state="readonly")

    def update_couleur_droite(self, valeur):
        val = int(valeur)
        triplet_droite = codes_couleur.calculer_triplet(val)
        code_hexa = codes_couleur.dec2hex(triplet_droite)

        self.__str_couleur_droite.set(code_hexa)

        nouvelle_couleur = [None, None, code_hexa]
        
        if self.__mode_ensemble.get():
            nouvelle_couleur[0] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(2.6923*val)))
            nouvelle_couleur[1] = codes_couleur.dec2hex(
                codes_couleur.calculer_triplet(int(1.9692*val)))
            
            # RVB
            self.__str_couleur_haut.set(nouvelle_couleur[0])
            self.__str_couleur_gauche.set(nouvelle_couleur[1])

            # hexa
            self.__code_haut_RVB.set(int(nouvelle_couleur[0][1:], 16))
            self.__code_gauche_RVB.set(int(nouvelle_couleur[1][1:], 16))

            # mise a jour des Entries des autres faces
            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[0])
            for i in range(3):
                self.__entry_RVB_haut[i].config(state="normal")
                self.__entry_RVB_haut[i].delete(0, tk.END)
                self.__entry_RVB_haut[i].insert(tk.END, triplet_temp[i])
                self.__entry_RVB_haut[i].config(state="readonly")
            
            triplet_temp = codes_couleur.hex2dec(nouvelle_couleur[1])
            for i in range(3):
                self.__entry_RVB_gauche[i].delete(0, tk.END)
                self.__entry_RVB_gauche[i].insert(tk.END, triplet_temp[i])

        else:
            # sinon, on modifie seulement l'actuelle
            nouvelle_couleur[0] = self.__str_couleur_haut.get()
            nouvelle_couleur[1] = self.__str_couleur_gauche.get()
        
        # on change la couleur du cube
        self.__cube_couleur.changer_couleur(nouvelle_couleur)
        # on modifie les entries
        for i in range(3):
            self.__entry_RVB_droite[i].config(state="normal")
            self.__entry_RVB_droite[i].delete(0, tk.END)
            self.__entry_RVB_droite[i].insert(tk.END, triplet_droite[i])
            self.__entry_RVB_droite[i].config(state="readonly")

    def confirmer_couleur(self):
        """
        Confirme la couleur choisie grace aux Scales.
        Les prochains cubes seront de cette couleur.
        """
        self.__couleur_cube = [
            self.__str_couleur_haut.get(),
            self.__str_couleur_gauche.get(),
            self.__str_couleur_droite.get()]
        self.__fenetre_couleur.destroy()


    # Gestion d'evenements

    def on_click(self, event):
        """En cas de clic sur le canvas"""
        current_coords = (event.x, event.y)
        converted_coords = self.grille.canvas_to_grille(current_coords)

        face_cliquee = self.canv.find_withtag("current")
        # face_cliquee est l'id de l'objet sur lequel on a clique

        if self.canv.type(face_cliquee) == "polygon":
            # si on a bien clique sur un polygone (une face de cube)
            id_cube = int(self.canv.gettags(face_cliquee)[0].split("_")[1])
            # tag 0 : "cube_idfaceduhaut"
            cube_tmp = self.rechercher_cube(id_cube)
            if cube_tmp is not None:
                x, y = cube_tmp.coords_to_3D()
                position3D = (x, y, cube_tmp.h)

                # On trouve quelle face etait-ce ('[0]' car c'est un tuple)
                if face_cliquee[0] == cube_tmp.haut:
                    self.placer_cube_haut(position3D)
                elif face_cliquee[0] == cube_tmp.gauche:
                    self.placer_cube_gauche(position3D)
                elif face_cliquee[0] == cube_tmp.droite:
                    self.placer_cube_droite(position3D)

        elif self.grille.is_in_grille(current_coords):
            # sinon ce n'est pas un polygone
            # on regarde si c'est dans la grille, si oui on place
            hauteur = 0
            self.placer_cube(
                self.grille.closest_point_up(converted_coords),hauteur)
            # par choix estethique, on ajuste le point 0.5 case plus haut
        if self.__cube_visu is not None:
            self.__cube_visu.priorite()

    def on_cube_click(self, event):
        """En cas de clic droit sur le canvas"""
        if self.__cube_select is not None:
            self.cacher_infos()
            # On deselectionne le cube d'avant
            self.__cube_select.deselection_cube()
            # On supprime les bindings des fleches directionnelles
            self.root.unbind("<Left>")
            self.root.unbind('<Right>')
            self.root.unbind('<Up>')
            self.root.unbind('<Down>')
            self.__cube_select = None

        current_coords = (event.x, event.y)
        converted_coords = self.grille.canvas_to_grille(current_coords)
        face_cliquee = self.canv.find_withtag("current")

        if self.canv.type(face_cliquee) == "polygon":
            # si on a bien clique sur un polygone (une face de cube)
            id_cube = int(self.canv.gettags(face_cliquee)[0].split("_")[1])
            # tag 0 : "cube_idfaceduhaut"
            cube_tmp = self.rechercher_cube(id_cube)
            if cube_tmp is not None:
                self.montrer_infos()
                coords_grille = cube_tmp.coords_to_3D()
                self.nom_cube.set("cube n°"+str(cube_tmp.numero))
                self.pos_cube.set("position |"
                    + " x : " + str(coords_grille[0])
                    + " y : " + str(coords_grille[1])
                    + " hauteur : "+str(cube_tmp.h))
                cube_tmp.selection_cube()
                self.__cube_select = cube_tmp
                # On bind les fleches directionnelles a self.deplacer_cube()
                self.root.bind('<Left>',
                    lambda event:self.deplacer_cube(event, plus_x = -1))
                self.root.bind('<Right>',
                    lambda event:self.deplacer_cube(event, plus_x= 1))
                self.root.bind('<Up>',
                    lambda event:self.deplacer_cube(event, plus_y = -1))
                self.root.bind('<Down>',
                    lambda event:self.deplacer_cube(event, plus_y = 1))
    
    def on_motion(self, event):
        if not self.__visualiser.get():
            if self.__cube_visu:
                self.__cube_visu.effacer()
                self.__cube_visu = None
            return
        d = self.grille.definition
        coords_event = (event.x, event.y)
        coords_grille = self.grille.canvas_to_grille(coords_event)

        if self.__cube_visu is None:
            # On cree le cube qui sera celui de la previsualisation
            if self.grille.is_in_grille(coords_event):
                # On place le cube si l'utilisateur entre dans la grille
                self.__cube_visu = cube.Cube(
                    self.canv,
                    self.grille,
                    coords_grille, # hauteur 0 par defaut
                    pcouleur=("#f2e6e3","#f2e6e3","#f2e6e3"))
                # on desactive le cube pour qu'on ne puisse par cliquer dessus
                self.__cube_visu.desactiver()
                self.__precoords = coords_event
        else:
            current_face = self.canv.find_withtag("current")
            # id du polygone sur lequel on est

            new_coords = self.grille.grille_to_canvas(
                self.grille.closest_point_up(
                    self.grille.canvas_to_grille(coords_event)))
            # peu elegant, mais on en a reellement besoin

            if self.canv.type(current_face) == "polygon":
                id_cube = int(self.canv.gettags(current_face)[0].split("_")[1])
                cube_tmp = self.rechercher_cube(id_cube)
                if cube_tmp is not None:
                    x, y = self.grille.canvas_to_grille(cube_tmp.coords)
                    # coordonnees 2D "reelles" du cube_tmp dans la grille
                    # on adapte la position en fonction de la face courante
                    if current_face[0] == cube_tmp.haut:
                        x -= 1
                        y -= 1
                    elif current_face[0] == cube_tmp.gauche:
                        y += 1
                    elif current_face[0] == cube_tmp.droite:
                        x +=1

                    new_coords2 = self.grille.grille_to_canvas((x, y))
                    delta_x = new_coords2[0] - self.__precoords[0]
                    delta_y = new_coords2[1] - self.__precoords[1]
                    self.canv.move("cube_"+str(self.__cube_visu.id),
                                    delta_x, delta_y)
                    self.__precoords = new_coords2

            elif self.grille.is_in_grille(coords_event):
                delta_x = new_coords[0] - self.__precoords[0]
                delta_y = new_coords[1] - self.__precoords[1]

                self.__precoords = new_coords
                self.canv.move("cube_"+str(self.__cube_visu.id),
                                delta_x, delta_y)


    def quitter(self):
        if messagebox.askyesno('Quit', 'Êtes-vous sûr de vouloir quitter ?'):
            self.root.quit()

    def montrer_infos(self):
        # Pour rendre les infos visibles
        self.info_nom.pack()
        self.info_pos.pack()
        self.zone_dessin.pack()
        self.supprimer_bouton.pack()

    def cacher_infos(self):
        """Cache les informations"""
        # Pack forget pour ne plus rendre les infos visibles
        self.info_nom.pack_forget()
        self.info_pos.pack_forget()
        self.zone_dessin.pack_forget()
        self.supprimer_bouton.pack_forget()

    def init_infos(self):
        """Affichage des informations"""
        self.nom_cube = tk.StringVar()
        self.pos_cube = tk.StringVar()

        self.zone_dessin = tk.Canvas(self.lf_infos, width=100, height=50, bd=8)
        self.fleche_haut = self.zone_dessin.create_line(
            60, 30, 60, 15, fill="black", width=10, arrow="last")
        self.fleche_bas = self.zone_dessin.create_line(
            60, 60, 60, 45, fill="black", width=10, arrow="first")
        self.fleche_gauche = self.zone_dessin.create_line(
            60, 38, 30, 38, fill="black", width=10, arrow="last")
        self.fleche_droite = self.zone_dessin.create_line(
            60, 38, 90, 38, fill="black", width=10, arrow="last")
        self.zone_dessin.pack()

        self.info_nom = tk.Label(self.lf_infos, textvariable=self.nom_cube)
        self.info_pos = tk.Label(self.lf_infos, textvariable=self.pos_cube)
        self.info_nom.pack()
        self.info_pos.pack()

        self.supprimer_bouton = tk.Button(
            self.lf_infos,
            text="Supprimer ce cube",
            command=self.supprimer_cube)
        self.supprimer_bouton.pack()

        self.lf_infos.pack(fill="both", expand="yes", side="right")


    def apropos(self):
        """
        Affiche des informations sur l'application
        dans une nouvelle fenetre
        """

        # On prend les infos de la root window pour
        #  positionner cette fenetre en haut a gauche
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        fenetre = tk.Toplevel(self.root)
        fenetre.resizable(width=False, height=False)
        fenetre.title("A propos")
        fenetre.geometry("+%d+%d" % (x, y))
        tk.Label(fenetre, text="Projet IHM L3 informatique").pack()
        tk.Label(fenetre, text="Copyright © 2020-2021").pack()
        label_dev = tk.LabelFrame(fenetre, text="Développeurs")
        tk.Label(label_dev,
            text="RESSEGUIER Mathieu et BOGADO GARCIA Maximino").pack()
        label_dev.pack()
        fenetre.grab_set()
        self.root.wait_window(fenetre)

    def ouvrir_documentation(self, event=None):
        try:
            webbrowser.open('doc.html')
        except webbrowser.Error:
            messagebox.showerror(
                title="Error",
                message="Erreur lors de l'ouverture du navigateur")

    def config(self):
        """Creation de la fenetre pour configurer la scene"""
        self.fenetre_config = tk.Toplevel(self.root)

        tk.Label(self.fenetre_config, text="Bienvenue !").pack()
        tk.Label(self.fenetre_config,
            text="Veuillez paramétrer votre scène").pack()

        # Config du canvas
        label_config = tk.LabelFrame(
            self.fenetre_config,
            text='Configuration du canvas')
        # 'sb' pour SpinBox
        self.sb_hauteur = tk.Spinbox(
            label_config,
            from_=100, to=1000, increment=10)
        self.sb_hauteur.grid(column=1, row=0, ipadx=5, pady=5)
        self.sb_hauteur.delete(0, tk.END)
        self.sb_hauteur.insert(0, 500)

        label_hauteur = tk.Label(label_config, text="Hauteur :")
        label_hauteur.grid(column=0, row=0, ipadx=5, pady=5)

        self.sb_largeur = tk.Spinbox(
            label_config,
            from_=100, to=1000, increment=10)
        self.sb_largeur.grid(column=1, row=1, ipadx=5, pady=5)
        self.sb_largeur.delete(0, tk.END)
        self.sb_largeur.insert(0, 500)
        
        label_largeur = tk.Label(label_config, text="Largeur :")
        label_largeur.grid(column=0, row=1, ipadx=5, pady=5)

        label_config.pack(padx=20)

        # Config de la grille
        label_grille = tk.LabelFrame(
            self.fenetre_config,
            text='Configuration de la grille')
        self.sb_nb_cases_x = tk.Spinbox(label_grille, from_=1, to=1000)
        self.sb_nb_cases_x.grid(column=1, row=0, ipadx=5, pady=5)
        self.sb_nb_cases_x.delete(0, tk.END)
        self.sb_nb_cases_x.insert(0, 10)

        label_nbcases_x = tk.Label(label_grille, text="Nombre de cases en x :")
        label_nbcases_x.grid(column=0, row=0, ipadx=5, pady=5)

        self.sb_nb_cases_y = tk.Spinbox(label_grille, from_=1, to=1000)
        self.sb_nb_cases_y.grid(column=1, row=1, ipadx=5, pady=5)
        self.sb_nb_cases_y.delete(0, tk.END)
        self.sb_nb_cases_y.insert(0, 10)

        label_nbcases_y = tk.Label(label_grille, text="Nombre de cases en y :")
        label_nbcases_y.grid(column=0, row=1, ipadx=5, pady=5)

        label_grille.pack(pady=20, padx=20)

        # Config de la taille d'un cube
        label_cube = tk.LabelFrame(
            self.fenetre_config,
            text='Configuration des cubes')
        self.sb_taille_cube = tk.Spinbox(label_cube, from_=10, to=1000)
        self.sb_taille_cube.grid(column=1, row=0, ipadx=5, pady=5)
        self.sb_taille_cube.delete(0, tk.END)
        self.sb_taille_cube.insert(0, 20)

        label_taille = tk.Label(label_cube,
            text="Choisissez la taille des cubes :")
        label_taille.grid(column=0, row=0, ipadx=5, pady=5)

        label_cube.pack(padx=20)

        # Construction de la scene avec les parametres choisis
        tk.Button(self.fenetre_config,
            text='Construire la scène',
            command=self.init_scene).pack(pady=10)

        self.fenetre_config.protocol("WM_DELETE_WINDOW", self.quitter)
        # pour gerer la fermeture avec la croix rouge et alt-f4

    def init_scene(self):
        # Stockage des parametres dans des variables
        canvas_l = int(self.sb_largeur.get())
        canvas_h = int(self.sb_hauteur.get())
        taille_y = int(self.sb_nb_cases_y.get())
        taille_x = int(self.sb_nb_cases_x.get())
        definition = int(self.sb_taille_cube.get())

        self.fenetre_config.destroy()
        self.root.deiconify()

        # LabelFrame qui contiendra les informations
        #  d'un cube lorsqu'on clique dessus
        self.lf_infos = tk.LabelFrame(
            self.root,
            text="Infos",
            padx=20, pady=20)
        self.init_infos()
        self.cacher_infos()

        # Menus

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, expand=True, fill=tk.X, anchor="n")

        # Menu fichier
        self.menu_fichier = tk.Menubutton(
            self.menu_frame,
            text="Fichier",
            underline=0,
            relief="raised")

        self.deroul_fichier = tk.Menu(self.menu_fichier, tearoff=False)
        self.deroul_fichier.add_command(label="Nouveau (Ctrl + N)",
                                        command=self.nouveau_fichier)
        self.deroul_fichier.add_command(label="Ouvrir (Ctrl + O)",
                                        command=self.ouvrir_fichier)
        self.deroul_fichier.add_command(label="Sauver (Ctrl + S)",
                                        command=self.sauver_fichier)
        self.deroul_fichier.add_command(label="Exporter (Ctrl + E)",
                                        command=self.sauver_svg)
        self.deroul_fichier.add_separator()
        self.deroul_fichier.add_command(label="Quitter (Alt + F4)",
                                        command=self.quitter)

        # Menu edition
        self.menu_edition = tk.Menubutton(
            self.menu_frame,
            text="Edition",
            underline=0,
            relief="raised")

        self.deroul_edition = tk.Menu(self.menu_edition, tearoff=False)
        self.__visualiser = tk.BooleanVar(value=True)
        self.deroul_edition.add_checkbutton(label="Visualiser (Ctrl + V)",
                                            variable=self.__visualiser)
        self.deroul_edition.add_command(label="Couleur (Ctrl + C)",
                                        command=self.ouvrir_fenetre_couleur)
        self.deroul_edition.add_command(label="Annuler (Ctrl + Z)",
                                        command=self.annuler_dernier_cube)
        self.root.bind("<Control-z>", self.annuler_dernier_cube)
        self.root.bind("<Delete>", self.supprimer_cube)
        self.root.bind("<Control-n>", self.nouveau_fichier)
        self.root.bind("<Control-o>", self.ouvrir_fichier)
        self.root.bind("<Control-e>", self.sauver_svg)
        self.root.bind("<Control-s>", self.sauver_fichier)
        self.root.bind("<Control-v>", self.toggle_visu)
        self.root.bind("<Control-c>", self.ouvrir_fenetre_couleur)
        self.root.bind("<F1>", self.ouvrir_documentation)

        # On desactive les options Sauver, Exporter et Annuler
        self.deroul_fichier.entryconfigure(2, state="disabled")
        self.deroul_fichier.entryconfigure(3, state="disabled")
        self.deroul_edition.entryconfigure(2, state="disabled")

        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        self.menu_fichier.config(menu=self.deroul_fichier)
        self.menu_fichier.pack(side=tk.LEFT)

        self.menu_edition.config(menu=self.deroul_edition)
        self.menu_edition.pack(side=tk.LEFT)

        # Menu aide
        self.menu_aide = tk.Menubutton(
            self.menu_frame,
            text="Aide",
            underline=0,
            relief="raised")
        self.deroul_aide = tk.Menu(self.menu_aide, tearoff=False)
        self.deroul_aide.add_command(label="Documentation (F1)",
                                     command=self.ouvrir_documentation)
        self.deroul_aide.add_command(label="A propos", command=self.apropos)
        self.menu_aide.config(menu=self.deroul_aide)
        self.menu_aide.pack(side=tk.RIGHT)

        # Canvas et grille

        self.canv = tk.Canvas(
            self.root,
            width=canvas_l,
            height=canvas_h,
            bg="white")
        self.texte_nb_cubes = self.canv.create_text(
            canvas_l-120,
            canvas_h-20,
            fill="black",
            text="Nombre de cubes dans la scene : " + str(self.NB_CUBES))
        self.canv.bind("<Motion>", self.on_motion)
        self.canv.bind("<Button-1>", self.on_click)
        self.canv.bind("<Button-3>", self.on_cube_click)
        self.canv.pack()

        self.grille = grille.Grille(self.canv, definition, taille_x, taille_y)


    # Constructeur de l'application

    def __init__(self):

        self.root = tk.Tk()
        self.root.withdraw()

        self.config()

        self.root.mainloop()


App()

exit(0)
