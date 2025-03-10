import streamlit as st
import qrcode
import io
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import StyledPilQRModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from utils.qr_styles import StarModuleDrawer, StyledPilImage2, TriRoundedRectangle
from utils.data_types import data_types, qr_fields
from utils.color import hex_to_rgba, make_image, make_transparent
from utils.logo import add_logo


qr_styles = {
            "Default": StyledPilQRModuleDrawer,
            "Square": SquareModuleDrawer,
            "Gapped Square": GappedSquareModuleDrawer,
            "Circle": CircleModuleDrawer,
            "Rounded": RoundedModuleDrawer,
            "Vertical Bars": VerticalBarsDrawer,
            "Horizontal Bars": HorizontalBarsDrawer,
            "Star": StarModuleDrawer
        }

eye_styles = {
            "Default": StyledPilQRModuleDrawer,
            "Square": SquareModuleDrawer,
            "Gapped Square": GappedSquareModuleDrawer,
            "Circle": CircleModuleDrawer,
            "Rounded": RoundedModuleDrawer,
            "Vertical Bars": VerticalBarsDrawer,
            "Horizontal Bars": HorizontalBarsDrawer,
            "Star": StarModuleDrawer,
            "Tri-Rounded Rectangle": TriRoundedRectangle,
        }

error_correction = {
    "7% (L)": qrcode.constants.ERROR_CORRECT_L,
    "15% (M)": qrcode.constants.ERROR_CORRECT_M,
    "25% (Q)": qrcode.constants.ERROR_CORRECT_Q,
    "30% (H)": qrcode.constants.ERROR_CORRECT_H
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
        col1, col2, col3 = st.columns(3)
        qr_size = col1.number_input("Size", value=500, step=1, min_value=50)
        qr_box_size = col2.number_input("Box Size", value=10, step=1, min_value=1, max_value=50)
        qr_border_size = col3.number_input("Border Size", value=1, step=1, min_value=1, max_value=10)
        
        col1, col2, col3 = st.columns(3)
        qr_eye_style_name = col1.selectbox("Eye Drawer", options=eye_styles.keys())
        qr_module_style_name = col2.selectbox("Module Drawer", options=qr_styles.keys())
        qr_error_correction = col3.selectbox("Error Correction", options=error_correction.keys(), index=3)

        qr_eye_style = eye_styles[qr_eye_style_name]
        qr_module_style = qr_styles[qr_module_style_name]
        qr_error_correction = error_correction[qr_error_correction]

        col1, col2, col3 = st.columns(3)
        qr_fill_color = col1.color_picker("Fill Color", value='#000000')
        qr_back_color = col2.color_picker("Background Color", value='#FFFFFF')
        qr_transparent = col3.checkbox("Transparent Background")

    if qr_transparent:
        qr_back_color = "#FFFFFF"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qr_error_correction,
        box_size=qr_box_size,
        border=qr_border_size,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_params = {"fill_color": qr_fill_color,
                 "back_color": qr_back_color}
    
    if qr_eye_style_name != "Default":
        qr_params["image_factory"] = StyledPilImage2
        qr_params["eye_drawer"] = qr_eye_style()
    if qr_module_style_name != "Default":
        qr_params["image_factory"] = StyledPilImage2
        qr_params["module_drawer"] = qr_module_style()

    img = qr.make_image(**qr_params).convert('RGBA')
    img = img.resize((qr_size, qr_size))

    # set the color in case image_factory is set to StypedPilImage2
    fill_color = hex_to_rgba(qr_fill_color, 255)
    back_color = hex_to_rgba(qr_back_color, 255)
    img = make_image(img, fill_color, back_color)
    
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
