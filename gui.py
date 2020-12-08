from tkinter import *
from math import pi
from PIL import ImageTk, Image

def gui_launcher(dic):              # fonction pour créer la fenêtre avec une frame de la classe Interface
    fenetre = Tk()                  
    fenetre.minsize(600, 400)
    fenetre.title("simulation.py - initialisation des paramètres")
    interface = Interface(fenetre, dic)
    interface.mainloop()
    return interface

class Interface(Frame):    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    def __init__(self, fenetre, dic):
        self.fenetre_to_destroy = fenetre
        Frame.__init__(self, fenetre)
        self.grid()
    
        ### Création de nos widgets

        # Schéma, nécessite le fichier 'schema.png' présent dans le dossier contenant les fichiers python
        # Source : https://www.youtube.com/watch?v=06MB1c7ucrk&feature=youtu.be
        try:
            self.img = Image.open("schema.png")
            self.img = self.img.resize((400, 300), Image.ANTIALIAS)
            self.my_img = ImageTk.PhotoImage(self.img)
            self.label_img = Label(image = self.my_img, width = 400, height = 300)
            self.label_img.grid(row =  0, column= 1, padx= 50)
        except:
            print("'schema.png' not found in directory")
        
        # Titre
        self.my_label1 = Label(self, text = "Paramètres du sytème",  font=("Courrier", 25))
        self.my_label1.grid(row = 1, pady=20)
################################################## Paramètres à redéfinir
        self.mc = DoubleVar()
        self.mc.set(dic["mc"])
        self.label_mc = Label(self, text="mc = masse de la charge [kg]")
        self.label_mc.grid(row = 2, sticky=W, padx= 50)        
        self.e_mc = Entry(self, textvariable=self.mc)
        self.e_mc.grid(row = 2, column = 1, sticky=W, pady=10)

        self.d_mc = DoubleVar()
        self.d_mc.set(dic["d_mc"])
        self.label_d_mc = Label(self, text="d = distance (finale) entre la charge et le centre [m]")
        self.label_d_mc.grid(row = 3, sticky=W, padx= 50)        
        self.e_d_mc = Entry(self, textvariable=self.d_mc)
        self.e_d_mc.grid(row = 3, column = 1, sticky=W, pady=10)

        self.v_mc = DoubleVar()
        self.v_mc.set(dic["v_mc"])
        self.label_v_mc = Label(self, text="v_mc = vitesse de déplacement de la charge mc [m/s]")
        self.label_v_mc.grid(row = 4, sticky=W, padx= 50)        
        self.e_v_mc = Entry(self, textvariable=self.v_mc)
        self.e_v_mc.grid(row = 4, column = 1, sticky=W, pady=10)

        self.angle_0 = DoubleVar()
        self.angle_0.set(round(dic["angle_0"]*180/pi, 2))
        self.label_angle_0 = Label(self, text="θ (t=0) = angle initial de la grue [degrés]")
        self.label_angle_0.grid(row = 5, sticky=W, padx= 50)        
        self.e_angle_0 = Entry(self, textvariable=self.angle_0)
        self.e_angle_0.grid(row = 5, column = 1, sticky=W, pady=10)
##############################################################################
        # Bouton 'Submit'
        self.bouton_cliquer = Button(self, text="Submit", command=self.submit, fg="#999999", font=("Courrier", 15, "bold"), relief=FLAT, highlightthickness=4, highlightcolor="black",  highlightbackground="black", borderwidth=4)
        self.bouton_cliquer.grid(row = 10, sticky=W, pady=20, padx= 50)
    
    def submit(self): # fonction pour récupérer les valeurs des 'Entry'
        self.mc = self.mc.get()        
        self.d_mc = self.d_mc.get()
        self.v_mc = self.v_mc.get()
        self.angle_0 = self.angle_0.get() * pi / 180
        self.fenetre_to_destroy.destroy()