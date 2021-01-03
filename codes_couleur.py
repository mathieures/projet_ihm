#Fonctions utiles pour la selection des couleurs

def calculer_triplet(nombre):
	B = nombre % 256
	V = (nombre // 256) % 256
	R = ((nombre // 256) // 256) % 256
	return (R,V,B)

def hex2dec(code):
	"""Convertit un code hexadecimal (commançant par #) en tuple d'entiers"""
	return [ int(code[j:j+2],16) for j in range(1,7,2) ]

def dec2hex(triplet):
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