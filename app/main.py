from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
import qrcode
from qrcode.constants import ERROR_CORRECT_L
import os
from datetime import datetime
from PIL import Image

fill = "#FFFFFF"
back = "#000000"
fill_path = ""

def fillColor():
    global fill
    fill_color = colorchooser.askcolor()
    fill = fill_color[1]
    print(fill)
    return fill

def backColor():
    global back
    back_color = colorchooser.askcolor()
    back = back_color[1]
    print(back)
    return back

def openFile():
    global file_path
    file_path = filedialog.askopenfilename(title="QRgenerator - Choisir un logo",
                                           filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("WEPB", "*.webp")])
    file = open(file_path, 'r')
    print(file_path)
    file.close

def Download():
    global fill, back, file_path
    url = url_input.get()
    extension_val = extension.get()
    fill_input_val = fill_input.get()
    back_input_val = back_input.get()
    now = datetime.now()

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
            logo_size = int(qr_width * 0.2)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Positionner le logo au centre
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # Coller le logo avec transparence si disponible
            if logo.mode in ("RGBA", "LA"):
                img.paste(logo, pos, mask=logo.split()[3])
            else:
                img.paste(logo, pos)

    chemin_dossier = os.path.expanduser("E:/python/QRcode/app/qrcode/")
    nom_fichier = name
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)

    # Créer le dossier s'il n'existe pas
    os.makedirs(chemin_dossier, exist_ok=True)

    # Enregistrer l’image
    img.save(chemin_complet)

def addLogo():
    logo_root = Tk()
    logo_root.title("QRcode generator - Ajouter un logo")

    Label(logo_root, text="Logo: ").place(x=20, y=15)
    file_btn = Button(logo_root, text="Choisir le logo", command=openFile)
    file_btn.place(x=100, y=15)
    quit_btn = Button(logo_root, text="Terminé", command=logo_root.destroy)
    quit_btn.place(x=20, y=45)

    logo_root.mainloop()

# _________________________
#|___________UI____________|
#Création de la fenêtre

extension_liste = ["PNG", "JPG", "WEPB"]
root = Tk()
root.title("QRcode generator")
root.geometry("600x200")
root.resizable(width=False, height=False)

#Partie URL

Label(root, text="URL du site: ").place(x=20, y=15)
url_input = Entry(root)
url_input.place(x=200, y=15, width=335)

#Partie couleur de remlplissage

Label(root, text="Couleur de remplissage: ").place(x=20, y=45)
#preview_fill = Canvas(root, width=20, height=20, bg=fill).place(x=165, y=45)
fill_button = Button(text="Choisir une couleur", command=fillColor)
fill_button.place(x=200, y=45)
Label(root, text="ou code HEX").place(x=325, y=45)
fill_input = Entry(root)
fill_input.place(x=415,y=45)


#Partie couleur de fond

Label(root, text="Couleur de fond: ").place(x=20, y=75)
#preview_back = Canvas(root, width=20, height=20, bg=back).place(x=165, y=75)
back_button = Button(root, text="Choisir une couleur", command=backColor)
back_button.place(x=200, y=75)
Label(root, text="ou code HEX").place(x=325, y=75)
back_input = Entry(root)
back_input.place(x=415, y=75)

#Partie sélection de l'extension

Label(root, text="Extension").place(x=20, y=105)
extension = ttk.Combobox(root, values=extension_liste)
extension.current(0)
extension.place(x=200, y=105)

#Ajouter un logo

logo_btn = Button(root, text="Ajouter un logo", command=addLogo)
logo_btn.place(x=20, y=135)

#Téléchargement

download = Button(root, text="Télécharger", command=Download)
download.place(x=470, y=135)

root.mainloop()