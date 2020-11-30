import Tkinter as tk

d = 36

def dessine():
	xx = 800/2
	yy = 800/5
	x = 800/2
	y = 800/5
	nb_cases_x = 10
	nb_cases_y = 10

	for i in range(nb_cases_y+1):
		canv.create_line(x,y,x+d*nb_cases_y,y+(d*nb_cases_y/2))
		x -= d
		y += d/2
	x = xx
	y = yy
	for j in range(nb_cases_x+1):
		canv.create_line(x,y,x-d*nb_cases_x,y+(d*nb_cases_x/2))
		x += d
		y += d/2

root = tk.Tk()
root.title("Test")
canv = tk.Canvas(root, width=800,height=800)
dessine()
canv.pack()
root.mainloop()
exit(0)
