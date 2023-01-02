from PIL import Image


def add_logo(img, uploaded_logo, base_width):
    logo = Image.open(uploaded_logo)

    # adjust image size
    w_percent = (base_width / float(logo.size[0]))
    h_size = int((float(logo.size[1]) * float(w_percent)))
    logo = logo.resize((base_width, h_size), Image.Resampling.LANCZOS)

    # set size of QR code
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos)
    return img
