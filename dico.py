class Dico(dict):
	"""Conteneur de toutes les coordonnees (referentiel de la grille) des cubes presents"""
	def __setitem__(self, pcoords_grille, phauteur):
		"""pcoords_grille est un tuple de deux entiers, representant une position (x,y)"""
		if self.get(pcoords_grille) is not None:
			self.get(pcoords_grille).append(phauteur)
		else:
			super().__setitem__(pcoords_grille, [phauteur])
		print("new Dico :",self)

	def vider(self):
		super().clear()

	def enlever(self,pcoords_grille,phauteur):
		self.get(pcoords_grille).remove(phauteur)
		if(self.get(pcoords_grille) == []): # si on a enleve le dernier de la liste, on enleve la cle
			del self[pcoords_grille]