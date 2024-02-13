"""
@author: Tuomas
"""
import tkinter as tk
from tkinter import messagebox
import sympy.parsing.sympy_parser as parser
import sympy as sym
import numpy as np
from sympy import Symbol
import math

#Ohjelmalla voi laskea lausekkeiden virheitä, yleistä virheen etenemislakia käyttäen.

_HEIGHT = 480
_WIDTH = 640

#Luodaan ikkuna    
root = tk.Tk()
root.minsize(_WIDTH, _HEIGHT) 
root.title("Helppoa ja kivaa")

muuttujat = ["x", "y", "z", "t", "h", "s"]
arvot = [0, 0, 0, 0, 0, 0]
virheet = [0, 0, 0, 0, 0, 0]
derivoidutlausekkeet = []
funktio = ""

def lue_arvot():
    """
    Luetaan muuttuja- ja virhekenttien syötteet.
    """
    for i in range(0, len(muuttujat)):
        arvot[i] = float(muuttujakentat[i].get())
        virheet[i] = float(virhekentat[i].get())

def derivoi_funktio(g):
    """
    Derivoi annetun funktion.
    
    Parameters
    ----------
    g : string
        Lauseke, jonka virhe halutaan laskea.
    """
    derivaatat = []
    #Muutetaan syötetty lauseke merkkijonosta sympy lausekkeeksi
    f = parser.parse_expr(g, evaluate=True)
    #Tyhjennetään tulostekentät
    tekstituloste.delete(1.0, tk.END)
    aputuloste.delete(1.0, tk.END)
    #Derivoidaan lauseke kaikkien muuttujien yli ja lisätään aputulosteeseen muuttujien nimet
    for i in range(0, len(muuttujat)):
        derivaatat.append(sym.diff(f, muuttujat[i]))
        aputuloste.insert(tk.INSERT, muuttujat[i])
        aputuloste.insert(tk.INSERT, ":")
        aputuloste.insert(tk.INSERT, "\n")
        
    global derivoidutlausekkeet
    derivoidutlausekkeet = derivaatat
    #Lisätään lopullinen lauseke tulostekenttään.
    tulostettava = "".join(map(lambda x: str(x)+"\n", derivoidutlausekkeet))
    tekstituloste.insert(tk.INSERT, tulostettava)
    
def laske_virheet(u):
    """
    Laskee annetun funktion virheen
    
    Parameters
    ----------
    u: string
        Lauseke, jonka virhe halutaan laskea.
    """
    derivoi_funktio(u)
    virhetermit = []
    f = parser.parse_expr(u, evaluate=True)
    tekstituloste.delete(1.0, tk.END)
    aputuloste.delete(1.0, tk.END)
    f_numpy = sym.lambdify([muuttujat], f, "numpy")
    tekstituloste.insert(tk.INSERT, f_numpy(arvot[:]))
    
    for j in range(0, len(muuttujat)):
        g = derivoidutlausekkeet[j]
        g_numpy = sym.lambdify([muuttujat], f, "numpy")
        virhetermit.append(float(g_numpy(arvot[:]))*float(virheet[j]))
    summa = 0
    
    for k in range(0, len(virhetermit)):
        summa += virhetermit[k]**2
    tekstituloste.insert(tk.INSERT, "\n Virhe on: \n" +str(math.sqrt(summa)))
def luo_valikot(asettelu):
    """
    Luo Tkinter valikon.
    
    Parameters
    ----------
    asettelu : Tkinter Frame
        Käyttöliittymän asetteluun liittyvä parametri.
    """
    
    valikko = tk.Menu(asettelu)
        
    laskuvalikko = tk.Menu(valikko, tearoff=0)
    valikko.add_cascade(label="Laske", menu=laskuvalikko)
    
    apuavalikko = tk.Menu(valikko, tearoff=0)
    valikko.add_cascade(label="Ohje", menu=apuavalikko)
    
    asettelu.config(menu=valikko)
    
    return laskuvalikko, apuavalikko
    
def luo_muuttujaasettelu(asettelu):
    """
    Luo Tkinter tekstikentät muuttujille.
    
    Parameters
    ----------
    asettelu : Tkinter Frame
        Käyttöliittymän asetteluun liittyvä parametri.
    """
    xkoord = 0
    muuttujakentat = []
        
    teksti = tk.Label(asettelu, text="ANNA MUUTTUJAT:")
    teksti.place(relx=0.25, relwidth=0.5)
        
    for i in muuttujat:
        muuttuja = tk.Label(asettelu, text =i+":", font=2, bg="#ffcccc")
        muuttuja.place(rely=0.1, relx=xkoord)
        muuttujakentta = tk.Entry(asettelu)
        muuttujakentat.append(muuttujakentta)
        muuttujakentta.place(rely=0.11, relx=xkoord+0.05, relwidth=0.1)
        muuttujakentta.insert(0, "0")
            
        xkoord += (1/len(muuttujat))
        
    return muuttujakentat
    
def luo_virheasettelu(asettelu):
    """
    Luo Tkinter tekstikentät virheille.
    
    Parameters
    ----------
    asettelu : Tkinter Frame
        Käyttöliittymän asetteluun liittyvä parametri.
    """
    xkoord = 0
    virhekentat = []
        
    teksti = tk.Label(asettelu, text="ANNA MUUTTUJIEN VIRHEET:")
    teksti.place(rely = 0.25, relx=0.25, relwidth=0.5)
        
    for i in muuttujat:
        muuttuja = tk.Label(asettelu, text =i+":", font=2, bg="#ffcccc")
        muuttuja.place(rely=0.35, relx=xkoord)
            
        virhekentta = tk.Entry(asettelu)
        virhekentat.append(virhekentta)
        virhekentta.place(rely=0.36, relx=xkoord+0.05, relwidth=0.1)
        virhekentta.insert(0, "0")
            
        xkoord += (1/len(muuttujat))
        
    return virhekentat
    
def luo_syoteasettelu(asettelu):
    """
    Luo Tkinter tekstikentän lausekkeelle.
    
    Parameters
    ----------
    asettelu : Tkinter Frame
        Käyttöliittymän asetteluun liittyvä parametri.
    """
        
    tekstikentta = tk.Entry(asettelu, font=30, fg="#ff66a3")
    tekstikentta.place(relheight=1, relwidth=1)
    tekstikentta.insert(0, "\t TERVETULOA ;)")
    return tekstikentta   
    

#Kehys tulosteasettelulle   
tulosteasettelu = tk.Frame(root, bg="#ffcccc", bd=5)
tulosteasettelu.place(rely=0.2, relwidth=1, relheight=0.8)

#Kehys syöteasettelulle 
syoteasettelu = tk.Frame(root, bg="#ffcccc", bd=5)
syoteasettelu.place(rely=0.1,relwidth=1, relheight=0.1)

tekstituloste = tk.Text(tulosteasettelu, font=20, fg="#ff66a3")
tekstituloste.place(relx=0.08,rely=0.5, relwidth=0.92, relheight=0.5)

aputuloste = tk.Text(tulosteasettelu, font=20, fg="#ff66a3")
aputuloste.place(rely=0.5, relwidth=0.05, relheight=0.5)

#Kutsutaan ikkunan luomiseen tarkoitettuja funktioita
tekstikentta = luo_syoteasettelu(syoteasettelu)

virhekentat = luo_virheasettelu(tulosteasettelu)

muuttujakentat = luo_muuttujaasettelu(tulosteasettelu)

valikot = luo_valikot(root)


def donothing():
    """
    Tulostaa ohjeita valikkoon laatikkoon tekstiä, kun se valitaan apuvalikosta.
    """
    tk.messagebox.showinfo("OHJEITA", "Syötä yläpalkkiin haluamasi lauseke käyttäen käytössä olevia muuttujia. Lausekkeen tulee käyttää samaa syntaksia kuin Pythonin. Esimerkiksi 5*x+exp(y**2). Tämän jälkeen valitse valikosta vaihtoehto derivoi. Ohjelma palauttaa lausekkeen osittaisderivaatat. Tämän jälkeen voit syöttää muuttuja- ja virhekenttiin arvot ja valita vaihtoehdon laske virheet.")
    
def deriv_apufunktio():
    """
    Apufunktio Tkiterin valikkotoiminnoille. Tekee derivoimiseen liittyvät toiminnot.
    """
    lue_arvot()
    funktio = tekstikentta.get()
    derivoi_funktio(funktio)

def lask_apufunktio():
    """
    Apufunktio Tkiterin valikkotoiminnoille. Tekee virheiden laskemiseen liittyvät toiminnot.
    """
    lue_arvot()
    funktio = tekstikentta.get()
    laske_virheet(funktio)

valikot[0].add_command(label="Derivaatat", command = lambda: deriv_apufunktio())
valikot[0].add_command(label="Virheet", command = lambda: lask_apufunktio() )
valikot[1].add_command(label="Ohje", command = lambda: donothing())
root.mainloop()
