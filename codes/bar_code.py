import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO


def main():
    st.title("Barcode")
    barcode_format = st.sidebar.selectbox("Barcode Formats", options=barcode.PROVIDED_BARCODES)
    barcode_data = st.sidebar.text_input("Data")
    barcode_text = st.sidebar.text_input("Barcode Text")

    rv = BytesIO()
    try:
        obj_barcode = barcode.get_barcode_class(barcode_format)
        obj_barcode(barcode_data, writer=ImageWriter()).write(rv, text=barcode_text)

        byte_im = rv.getvalue()
        st.image(byte_im)

        st.download_button(label="Download PNG",
                           data=byte_im,
                           file_name="barcode.png",
                           mime="image/png")
    except Exception as e:
        st.error(str(e))


if __name__ == '__main__':
    main()
