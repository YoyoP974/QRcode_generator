import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_L

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QRcode generator")
        self.root.geometry("600x200")
        self.root.resizable(width=False, height=False)

        self.fill = "#FFFFFF"
        self.back = "#000000"
        self.file_path = ""
        self.taille = "Petit"
        self.extension_liste = ["PNG", "JPG", "WEBP"]

        self.setup_ui()

    def setup_ui(self):
        # URL
        Label(self.root, text="URL du site: ").place(x=20, y=15)
        self.url_input = Entry(self.root)
        self.url_input.place(x=200, y=15, width=335)

        # Couleur remplissage
        Label(self.root, text="Couleur de remplissage: ").place(x=20, y=45)
        self.preview_fill = Canvas(self.root, width=20, height=20, bg=self.fill)
        self.preview_fill.place(x=550, y=45)
        Button(self.root, text="Choisir une couleur", command=self.choose_fill_color).place(x=200, y=45)
        Label(self.root, text="code HEX: ").place(x=330, y=45)
        self.fill_input = Entry(self.root)
        self.fill_input.place(x=415, y=45)
        self.fill_input.insert(0, self.fill)
        self.fill_input.bind("<KeyRelease>", self.update_fill_preview)

        # Couleur fond
        Label(self.root, text="Couleur de fond: ").place(x=20, y=75)
        self.preview_back = Canvas(self.root, width=20, height=20, bg=self.back)
        self.preview_back.place(x=550, y=75)
        Button(self.root, text="Choisir une couleur", command=self.choose_back_color).place(x=200, y=75)
        Label(self.root, text="code HEX: ").place(x=330, y=75)
        self.back_input = Entry(self.root)
        self.back_input.place(x=415, y=75)
        self.back_input.insert(0, self.back)
        self.back_input.bind("<KeyRelease>", self.update_back_preview)

        # Extension
        Label(self.root, text="Extension").place(x=20, y=105)
        self.extension = ttk.Combobox(self.root, values=self.extension_liste, state="readonly")
        self.extension.current(0)
        self.extension.place(x=200, y=105)

        # Boutons
        Button(self.root, text="Ajouter un logo", command=self.add_logo).place(x=20, y=135)
        Button(self.root, text="Réinitialiser", command=self.reset).place(x=250, y=135)
        Button(self.root, text="Télécharger", command=self.download).place(x=470, y=135)

    def choose_fill_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.fill = color[1]
            self.preview_fill.config(bg=self.fill)
            self.fill_input.delete(0, END)
            self.fill_input.insert(0, self.fill)

    def choose_back_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.back = color[1]
            self.preview_back.config(bg=self.back)
            self.back_input.delete(0, END)
            self.back_input.insert(0, self.back)

    def update_fill_preview(self, event=None):
        val = self.fill_input.get()
        if self.is_valid_hex(val):
            self.fill = val
            self.preview_fill.config(bg=self.fill)

    def update_back_preview(self, event=None):
        val = self.back_input.get()
        if self.is_valid_hex(val):
            self.back = val
            self.preview_back.config(bg=self.back)

    @staticmethod
    def is_valid_hex(val):
        if val.startswith("#") and len(val) in (4, 7):
            try:
                int(val[1:], 16)
                return True
            except ValueError:
                return False
        return False

    def open_file(self):
        path = filedialog.askopenfilename(
            title="QRgenerator - Choisir un logo",
            initialdir=os.path.expanduser("~/Pictures"),
            filetypes=[("Images", "*.png *.jpg *.webp")]
        )
        if path:
            self.file_path = path
            print(f"Logo choisi : {self.file_path}")

    def add_logo(self):
        logo_win = Toplevel(self.root)
        logo_win.title("Ajouter un logo")
        logo_win.geometry("200x115")
        logo_win.resizable(False, False)
        logo_win.transient(self.root)
        logo_win.grab_set()
        logo_win.focus_force()

        Label(logo_win, text="Logo: ").place(x=20, y=15)
        Button(logo_win, text="Choisir le logo", command=self.open_file).place(x=100, y=15)

        self.taille_combo = ttk.Combobox(logo_win, values=["Petit", "Grand"], state="readonly")
        self.taille_combo.current(0)
        self.taille_combo.place(x=20, y=45)

        Button(logo_win, text="Terminé", command=logo_win.destroy).place(x=20, y=75)

    def reset(self):
        if messagebox.askokcancel("Réinitialiser", "Voulez-vous vraiment réinitialiser tous les paramètres ?"):
            self.fill = "#FFFFFF"
            self.back = "#000000"
            self.file_path = ""
            self.url_input.delete(0, END)
            self.fill_input.delete(0, END)
            self.fill_input.insert(0, self.fill)
            self.back_input.delete(0, END)
            self.back_input.insert(0, self.back)
            self.preview_fill.config(bg=self.fill)
            self.preview_back.config(bg=self.back)
            print("Paramètres réinitialisés")

    def download(self):
        url = self.url_input.get().strip()
        if not url:
            messagebox.showerror("Erreur", "L'URL ne peut pas être vide.")
            return

        fill = self.fill_input.get()
        back = self.back_input.get()
        if not self.is_valid_hex(fill) or not self.is_valid_hex(back):
            messagebox.showerror("Erreur", "Les codes couleurs doivent être des codes HEX valides.")
            return

        ext = self.extension.get().lower()
        now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"{now_str}.{ext}"

        qr = qrcode.QRCode(
            version=4,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=3
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=back).convert("RGBA")

        # Ajouter logo si disponible
        if self.file_path:
            logo_size_ratio = 0.2 if self.taille_combo.get() == "Petit" else 0.3
            logo = Image.open(self.file_path).convert("RGBA")
            qr_width, qr_height = img.size
            logo_size = int(qr_width * logo_size_ratio)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, pos, mask=logo)

        # Dossier par défaut où enregistrer
        save_dir = os.path.expanduser("~/Downloads/QRcodes")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        try:
            img.save(save_path)
            messagebox.showinfo("Succès", f"QR code enregistré sous :\n{save_path}")
            print(f"QR code sauvegardé dans {save_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le QR code.\n{e}")

if __name__ == "__main__":
    root = Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
