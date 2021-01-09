class Dico(dict):
    """
    Conteneur de toutes les coordonnees (referentiel de la grille)
    des cubes presents dans la scene.
    """
    def __setitem__(self, pcoords_grille, phauteur):
        """Ajoute une valeur au dictionnaire :
        Si la cle n'existe pas, elle est creee et une liste d'1 element
        est associee a celle-ci.
        """
        # pcoords_grille est une position : un tuple de deux entiers (x,y)
        if self.get(pcoords_grille) is not None:
            self.get(pcoords_grille).append(phauteur)
        else:
            super().__setitem__(pcoords_grille, [phauteur])

    def vider(self):
        """Efface toutes les cles et valeurs du dictionnaire."""
        super().clear()

    def enlever(self,pcoords_grille,phauteur):
        """
        Similaire a la methode 'remove' de la classe list.
        Cette methode enleve la valeur phauteur de la liste associee
        a la cle pcoords_grille dans le dictionnaire.
        """
        self.get(pcoords_grille).remove(phauteur)
        if not self.get(pcoords_grille):
            # si on a enleve le dernier de la liste, on enleve la cle
            del self[pcoords_grille]