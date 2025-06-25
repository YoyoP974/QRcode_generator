from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
import qrcode
from qrcode.constants import ERROR_CORRECT_L
import os
from datetime import datetime
from PIL import Image, ImageTk

fill = "#000000"
back = "#FFFFFF"
file_path = ""
url = ""
taille_liste = ["Petit", "Grand"]
taille = ""
taille_val = ""

def fillColor():
    global fill
    fill_color = colorchooser.askcolor()
    if fill_color[1] is not None:
        fill = fill_color[1]
        preview_fill.config(bg=fill)
        fill_input.delete(0, END)
        fill_input.insert(0, fill)
    print(fill)
    return fill

def backColor():
    global back
    back_color = colorchooser.askcolor()
    if back_color[1] is not None:
        back = back_color[1]
        preview_back.config(bg=back)
        back_input.delete(0, END)
        back_input.insert(0, back)
    print(back)
    return back

def update_fill_preview(event=None):
    global fill
    val = fill_input.get()
    if val.startswith("#") and (len(val) == 7 or len(val) == 4):  # simple validation HEX
        fill = val
        preview_fill.config(bg=fill)

def update_back_preview(event=None):
    global back
    val = back_input.get()
    if val.startswith("#") and (len(val) == 7 or len(val) == 4):
        back = val
        preview_back.config(bg=back)

def openFile():
    global file_path
    file_path = filedialog.askopenfilename(title="QRgenerator - Choisir un logo",
                                           initialdir="~/Pictures",
                                           filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("WEPB", "*.webp")])
    file = open(file_path, 'r')
    print(file_path)
    file.close

def Download():
    global fill, back, file_path, url, taille, taille_liste, taille_val
    url = url_input.get()
    extension_val = extension.get()
    fill_input_val = fill_input.get()
    back_input_val = back_input.get()
    now = datetime.now()

    #user_file_path = filedialog.askopenfilename(title="QRgenerator - Télécharger")
    #user_file = open(user_file_path, 'r')
    #print(file_path)
    #user_file.close

    if fill_input_val != "":
        fill = fill_input_val

    if back_input_val != "":
        back = back_input_val

    if extension_val == extension_liste[0]:
        name = "{}.png".format(now.strftime("%Y-%m-%d-%H-%M-%S"))
    elif extension_val == extension_liste[1]:
        name = "{}.jpg".format(now.strftime("%Y-%m-%d-%H-%M-%S"))
    elif extension_val == extension_liste[2]:
        name = "{}.webp".format(now.strftime("%Y-%m-%d-%H-%M-%S"))

    

    qr = qrcode.QRCode(
    version=4,
    error_correction=ERROR_CORRECT_L,
    box_size=10,
    border=3
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color = fill, back_color = back)

    if file_path != "":
            logo = Image.open(file_path)

            qr_width, qr_height = img.size
            if taille_val == taille_liste[0]:
                logo_size = int(qr_width * 0.2)
            elif taille_val == taille_liste[1]:
                logo_size = int(qr_width * 0.3)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Positionner le logo au centre
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # Coller le logo avec transparence si disponible
            if logo.mode in ("RGBA", "LA"):
                img.paste(logo, pos, mask=logo.split()[3])
            else:
                img.paste(logo, pos)

    chemin_dossier = os.path.expanduser("E:/python/QRcode/app/qrcode/")
    download_chemin_dossier = os.path.expanduser("~/Downloads")
    nom_fichier = name
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)
    download_chemin_complet = os.path.join(download_chemin_dossier, nom_fichier)

    # Créer le dossier s'il n'existe pas
    os.makedirs(chemin_dossier, exist_ok=True)
    os.makedirs(download_chemin_dossier, exist_ok=True)

    print(url)
    print(fill)
    print(back)
    print(extension_val)
    print(name)

    # Enregistrer l’image
    img.save(chemin_complet)
    img.save(download_chemin_complet)
    messagebox.showinfo("Télécgarement", "Le QRcode a été télécgargé dans votre de dossier Télécgargements")

def addLogo():
    global taille, logo_root
    logo_root = Toplevel(root)
    logo_root.title("QRcode generator - Ajouter un logo")
    logo_root.geometry("200x115")
    logo_root.resizable(width=False, height=False)
    logo_root.iconbitmap(r"E:\python\QRcode\app\logo_qrcode_generator.ico")

    logo_root.transient(root)  # Fenêtre secondaire liée à root
    logo_root.grab_set()       # Modal : empêche d'interagir avec root tant que logo_root est ouvert
    logo_root.focus_force()    # Force le focus sur la fenêtre secondaire

    Label(logo_root, text="Logo: ").place(x=20, y=15)
    file_btn = Button(logo_root, text="Choisir le logo", command=openFile)
    file_btn.place(x=100, y=15)
    taille = ttk.Combobox(logo_root, values=taille_liste)
    taille.current(0)
    taille.place(x=20, y=45)
    quit_btn = Button(logo_root, text="Terminé", command=saveLogo)
    quit_btn.place(x=20, y=75)

    logo_root.mainloop()

def saveLogo ():
    global taille_val, logo_root
    taille_val = taille.get()
    logo_root.destroy()

def reinitialiser():
    global fill, back, file_path, url
    reponse = messagebox.askokcancel("QRcode generator - Réinitialiser", "Voulez-vous vraiment réinitialiser tous les paramètres ?")
    if reponse:
        print("Réinitialisation des paramètres")
        fill_input.delete(0, END)
        fill = "#000000"
        back_input.delete(0, END)
        back = "#FFFFFF"
        url_input.delete(0, END)
        url = ""
        file_path = ""

def About():
    about_root = Toplevel(root)
    about_root.title("QRcode generator - A propos")
    about_root.geometry("250x160")
    about_root.resizable(width=False, height=False)
    about_root.iconbitmap(r"E:\python\QRcode\app\logo_qrcode_generator.ico")

    about_root.transient(root)  # Fenêtre secondaire liée à root
    about_root.grab_set()       # Modal : empêche d'interagir avec root tant que about_root est ouvert
    about_root.focus_force()    # Force le focus sur la fenêtre secondaire

    
    pil_image = Image.open(r"E:\python\QRcode\app\logo_qrcode_generator.png")
    pil_image = pil_image.resize((50, 50))  # Redimensionner à 50x50 pixels

    logo = ImageTk.PhotoImage(pil_image)

    logo_canva = Canvas(about_root, width=50, height=50)
    item = logo_canva.create_image(25, 25, image = logo)
     
    #Rajouter cette ligne
    logo_canva.image = logo
    logo_canva.pack()
    Label(about_root, text="QRcode génerator").pack()
    Label(about_root, text="crée par PIA Yoni").pack()
    Label(about_root, text="2025").pack()
    Label(about_root, text="Email: yoni.pia54@gmail.com").pack()
    Label(about_root, text="Github: https://github.com/YoyoP974/").pack()


# _________________________
#|___________UI____________|
#Création de la fenêtre

extension_liste = ["PNG", "JPG", "WEBP"]
root = Tk()
root.title("QRcode generator")
root.geometry("600x200")
root.resizable(width=False, height=False)
root.iconbitmap(r"E:\python\QRcode\app\logo_qrcode_generator.ico")

#Partie URL

Label(root, text="URL du site: ").place(x=20, y=15)
url_input = Entry(root)
url_input.place(x=200, y=15, width=335)

#Partie couleur de remlplissage

Label(root, text="Couleur de remplissage: ").place(x=20, y=45)
preview_fill = Canvas(root, width=20, height=20, bg=fill)
preview_fill.place(x=550, y=45)
fill_button = Button(text="Choisir une couleur", command=fillColor)
fill_button.place(x=200, y=45)
Label(root, text="code HEX: ").place(x=330, y=45)
fill_input = Entry(root)
fill_input.place(x=415,y=45)

fill_input.bind("<KeyRelease>", update_fill_preview)


#Partie couleur de fond

Label(root, text="Couleur de fond: ").place(x=20, y=75)
preview_back = Canvas(root, width=20, height=20, bg=back)
preview_back.place(x=550, y=75)
back_button = Button(root, text="Choisir une couleur", command=backColor)
back_button.place(x=200, y=75)
Label(root, text="code HEX: ").place(x=330, y=75)
back_input = Entry(root)
back_input.place(x=415, y=75)

back_input.bind("<KeyRelease>", update_back_preview)

#Partie sélection de l'extension

Label(root, text="Extension").place(x=20, y=105)
extension = ttk.Combobox(root, values=extension_liste)
extension.current(0)
extension.place(x=200, y=105)

#Ajouter un logo

logo_btn = Button(root, text="Ajouter un logo", command=addLogo)
logo_btn.place(x=20, y=135)

#Réinitialiser
rein_btn = Button(root, text="Réinitialiser", command=reinitialiser)
rein_btn.place(x=250, y=135)

#Téléchargement

download = Button(root, text="Télécharger", command=Download)
download.place(x=470, y=135)

#About 

about_bnt = Button(root, text="A propos", command=About)
about_bnt.place(x=20, y=165)

root.mainloop()