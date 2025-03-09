import streamlit as st
from streamlit_option_menu import option_menu
from src import qr, bar_code


def main():
    selected = option_menu(None, ["QR Code", "Barcode"],
                           icons=['qr-code-scan', 'upc-scan'],
                           menu_icon="cast", default_index=0, orientation="horizontal")
    if selected == "QR Code":
        qr.main()
    elif selected == "Barcode":
        bar_code.main()


if __name__ == '__main__':
    st.set_page_config(page_title="QR Code and Barcode Generator",
                       menu_items={
                           'Get Help': 'https://github.com/kavehbc/qr-barcode-generator',
                           'Report a bug': "https://github.com/kavehbc/qr-barcode-generator",
                           'About': """
                               # QR Code and Barcode Generator

                               Version 2.0 - Kaveh Bakhtiyari
                               """
                       }
                       )
    main()
