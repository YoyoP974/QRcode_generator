from tkinter import *
from tkinter import ttk, colorchooser, filedialog, messagebox
import qrcode
from qrcode.constants import ERROR_CORRECT_L
import os
from datetime import datetime
from PIL import Image, ImageTk

# Variables globales
fill = "#000000"
back = "#FFFFFF"
file_path = ""
url = ""
taille_var = StringVar(value="Petit")  # Stocke la taille sélectionnée
extension_liste = ["PNG", "JPG", "WEBP"]

# Fonctions
def fillColor():
    global fill
    color = colorchooser.askcolor()[1]
    if color:
        fill = color
        fill_input.delete(0, END)
        fill_input.insert(0, fill)
        preview_fill.config(bg=fill)

def backColor():
    global back
    color = colorchooser.askcolor()[1]
    if color:
        back = color
        back_input.delete(0, END)
        back_input.insert(0, back)
        preview_back.config(bg=back)

def update_fill_preview(event=None):
    global fill
    val = fill_input.get()
    if val.startswith("#") and len(val) in [4, 7]:
        fill = val
        preview_fill.config(bg=fill)

def update_back_preview(event=None):
    global back
    val = back_input.get()
    if val.startswith("#") and len(val) in [4, 7]:
        back = val
        preview_back.config(bg=back)

def openFile():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Choisir un logo",
        filetypes=[("Images", "*.png;*.jpg;*.webp")]
    )

def Download():
    global file_path
    url = url_input.get()
    ext = extension.get()
    now = datetime.now()

    if not url.strip():
        messagebox.showwarning("Erreur", "Veuillez entrer une URL.")
        return

    filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    ext_map = {"PNG": "png", "JPG": "jpg", "WEBP": "webp"}
    file_ext = ext_map.get(ext, "png")
    name = f"{filename}.{file_ext}"

    # Construction du QR Code
    qr = qrcode.QRCode(version=4, error_correction=ERROR_CORRECT_L, box_size=10, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back)

    if file_path:
        logo = Image.open(file_path)
        qr_width, qr_height = img.size

        size_pct = 0.2 if taille_var.get() == "Petit" else 0.3
        logo_size = int(qr_width * size_pct)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        if logo.mode in ("RGBA", "LA"):
            img.paste(logo, pos, mask=logo.split()[3])
        else:
            img.paste(logo, pos)

    # Enregistrement
    dossier = os.path.expanduser("~/Downloads")
    os.makedirs(dossier, exist_ok=True)
    path = os.path.join(dossier, name)
    img.save(path)
    messagebox.showinfo("Téléchargement", f"QR Code téléchargé dans :\n{path}")

def addLogo():
    logo_root = Toplevel(root)
    logo_root.title("Ajouter un logo")
    logo_root.geometry("250x130")
    logo_root.resizable(False, False)

    Label(logo_root, text="Logo:").pack(pady=5)
    Button(logo_root, text="Choisir un logo", command=openFile).pack()
    Label(logo_root, text="Taille du logo:").pack(pady=5)
    combo = ttk.Combobox(logo_root, values=["Petit", "Grand"], textvariable=taille_var)
    combo.pack()
    combo.current(0)
    Button(logo_root, text="Terminé", command=logo_root.destroy).pack(pady=5)

def reinitialiser():
    global fill, back, file_path
    if messagebox.askokcancel("Réinitialiser", "Voulez-vous réinitialiser les paramètres ?"):
        fill = "#000000"
        back = "#FFFFFF"
        file_path = ""
        url_input.delete(0, END)
        fill_input.delete(0, END)
        back_input.delete(0, END)
        preview_fill.config(bg=fill)
        preview_back.config(bg=back)

def About():
    about_root = Toplevel(root)
    about_root.title("À propos")
    about_root.geometry("250x160")
    about_root.resizable(False, False)

    logo = Image.open("E:/python/QRcode/app/logo_qrcode_generator.png")
    logo = logo.resize((50, 50))
    logo_img = ImageTk.PhotoImage(logo)

    logo_canvas = Canvas(about_root, width=50, height=50)
    logo_canvas.create_image(25, 25, image=logo_img)
    logo_canvas.image = logo_img
    logo_canvas.pack()

    Label(about_root, text="QRcode Generator").pack()
    Label(about_root, text="Créé par PIA Yoni").pack()
    Label(about_root, text="2025").pack()
    Label(about_root, text="Email: yoni.pia54@gmail.com").pack()
    Label(about_root, text="GitHub: github.com/YoyoP974").pack()

# ________________________
# Interface principale
root = Tk()
root.title("QRcode Generator")
root.geometry("600x200")
root.resizable(False, False)
root.iconbitmap("E:/python/QRcode/app/logo_qrcode_generator.ico")

Label(root, text="URL du site:").place(x=20, y=15)
url_input = Entry(root)
url_input.place(x=200, y=15, width=335)

Label(root, text="Couleur de remplissage:").place(x=20, y=45)
preview_fill = Canvas(root, width=20, height=20, bg=fill)
preview_fill.place(x=550, y=45)
Button(root, text="Choisir une couleur", command=fillColor).place(x=200, y=45)
Label(root, text="Code HEX:").place(x=330, y=45)
fill_input = Entry(root)
fill_input.place(x=415, y=45)
fill_input.bind("<KeyRelease>", update_fill_preview)

Label(root, text="Couleur de fond:").place(x=20, y=75)
preview_back = Canvas(root, width=20, height=20, bg=back)
preview_back.place(x=550, y=75)
Button(root, text="Choisir une couleur", command=backColor).place(x=200, y=75)
Label(root, text="Code HEX:").place(x=330, y=75)
back_input = Entry(root)
back_input.place(x=415, y=75)
back_input.bind("<KeyRelease>", update_back_preview)

Label(root, text="Extension:").place(x=20, y=105)
extension = ttk.Combobox(root, values=extension_liste)
extension.current(0)
extension.place(x=200, y=105)

Button(root, text="Ajouter un logo", command=addLogo).place(x=20, y=135)
Button(root, text="Réinitialiser", command=reinitialiser).place(x=250, y=135)
Button(root, text="Télécharger", command=Download).place(x=470, y=135)
Button(root, text="À propos", command=About).place(x=20, y=165)

root.mainloop()
