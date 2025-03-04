import streamlit as st
import qrcode
import io
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import StyledPilQRModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from utils.data_types import data_types, qr_fields
from utils.color import hex_to_rgba, make_transparent
from utils.logo import add_logo


qr_styles = {
            # "StyledPilQRModuleDrawer": StyledPilQRModuleDrawer,
            "SquareModuleDrawer": SquareModuleDrawer,
            "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
            "CircleModuleDrawer": CircleModuleDrawer,
            "RoundedModuleDrawer": RoundedModuleDrawer,
            "VerticalBarsDrawer": VerticalBarsDrawer,
            "HorizontalBarsDrawer": HorizontalBarsDrawer
        }

def main():
    st.title("QR Code")
    qr_data_types = st.sidebar.selectbox("QR Template", options=data_types.keys())

    input_fields = []
    for item in qr_fields[qr_data_types].keys():
        input_fields.append(st.sidebar.text_input(item, value=qr_fields[qr_data_types][item]))

    qr_data_replaced = str(data_types[qr_data_types])
    for item in input_fields:
        qr_data_replaced = qr_data_replaced.replace("@@", item, 1)

    with st.expander("Advanced Parameters"):
        qr_data = st.text_area("QR Data", qr_data_replaced, height=250)
        col1, col2, col3, col4 = st.columns(4)
        qr_size = col1.number_input("Size", value=500, step=1, min_value=50)
        qr_box_size = col2.number_input("Box Size", value=10, step=1, min_value=1, max_value=50)
        qr_border_size = col3.number_input("Border Size", value=1, step=1, min_value=1, max_value=10)
        qr_style_name = col4.selectbox("Drawer Style", options=qr_styles.keys())
        qr_style = qr_styles[qr_style_name]
        col1, col2, col3 = st.columns(3)
        qr_fill_color = col1.color_picker("Fill Color", value='#000000')
        qr_back_color = col2.color_picker("Background Color", value='#FFFFFF')
        qr_transparent = col3.checkbox("Transparent Background")

    if qr_transparent:
        qr_back_color = "#FFFFFF"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr_box_size,
        border=qr_border_size,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=qr_style(),
                        fill_color=qr_fill_color,
                        back_color=qr_back_color).convert('RGBA')
    img = img.resize((qr_size, qr_size))

    # logo file
    uploaded_logo = st.sidebar.file_uploader("Logo", accept_multiple_files=False, type=['png', 'jpg'])
    if uploaded_logo is not None:
        # taking base width for the logo
        base_width = st.sidebar.number_input("Logo Size", value=100, min_value=50, step=1)
        img = add_logo(img, uploaded_logo, base_width)

    if qr_transparent:
        # output opaque_pixel = (0, 0, 0, 255)
        opaque_pixel = hex_to_rgba(qr_fill_color, 255)
        transparent_pixel = (255, 255, 255, 0)

        # invert colors and set alpha color
        img = make_transparent(img, opaque_pixel, transparent_pixel)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(byte_im)
    st.download_button(label="Download PNG",
                       data=byte_im,
                       file_name="qr_code.png",
                       mime="image/png")


if __name__ == '__main__':
    main()
