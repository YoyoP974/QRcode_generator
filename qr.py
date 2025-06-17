import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H

url = input("Entrez l'URL du site: ")
fill = input("Couleur de remplissage(code HEX): ")
back = input("Couleur de fond(code HEX): ")

logo = Image.open("python_logo.png")

qr = qrcode.QRCode(
    version=4,  # ou plus si l'URL est longue
    error_correction=ERROR_CORRECT_H,
    box_size=10,
    border=4
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color = "#{}".format(fill), back_color = "#{}".format(back)).convert('RGB')

basewidth = 100

# Redimensionner le logo à 20% du QR code
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

img.save("qrcode.png")