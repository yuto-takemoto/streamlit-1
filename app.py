##streamlit
import streamlit as st
import glob
from PIL import Image
import numpy as np
import cv2

## layout
st.set_page_config(layout="wide")
st.title('Image viewer')
##read image
path = st.text_input('Image path')
col1, col2 = st.beta_columns(2)
#path = r'C:\takemoto\1.research\take_REC_1-2_180810-1_2018081000115\take_REC_1-2_180810-1_2018081000115_x000000y000000-04x-Tiling8x8'


@st.cache(suppress_st_warning=True)
def make_list():
    global til_list, frm_list, bind_til_list
    img_list = glob.glob(time_list[int(frame)] + '/*.png')

    ## bind image
    bind_til_list = []
    for pas in range(len(time_list)):
        not_bind_til_list = []
        img_list = glob.glob(time_list[int(pas)] + '/*.png')
        for i in range(len(img_list)):
            temp_img = cv2.imread(img_list[i])
            temp_img2 = np.array(temp_img)
            not_bind_til_list.append(temp_img2)
        x1 = np.array(not_bind_til_list)

        l = int(np.sqrt(len(img_list)))
        a = np.arange(0, l ** 2, l)
        b = np.arange(l, (l ** 2 + l), l)
        til_dim = np.array([a, b])
        row_list = []
        for row in range(l):
            til_img1 = np.hstack(x1[til_dim[0, row]:til_dim[1, row]])
            row_list.append(til_img1)
        til_img2 = np.vstack(row_list)
        til_img3 = Image.fromarray(til_img2)
        til_img4 = til_img3.resize((500, 500))
        bind_til_list.append(til_img4)

    # read each tilling image
    til_list = []
    for tile in range(len(img_list)):
        frm_list = []
        for pas in range(len(time_list)):
            img_list = glob.glob(time_list[int(pas)] + '/*.png')
            til1 = cv2.imread(img_list[tile])
            til2 = Image.fromarray(til1)
            til2 = til2.resize((500, 500))
            frm_list.append(til2)
        til_list.append(frm_list)

    return frm_list, til_list, bind_til_list

if path:
    time_list = glob.glob(path + '/**/Ph')
    frame = st.sidebar.slider('Frame', min_value=0, max_value=(len(time_list)-1), step=1)

    frm_list, til_list, bind_til_list = make_list()
    # Display
    #col1.title("All images")
    col1.markdown("<h1 style='text-align: center; color: black;'>All images</h1>", unsafe_allow_html=True)
    col1.image(bind_til_list[frame], width=200, use_column_width=True)

    SAVE_GIF1 = col1.button("SAVE GIF", key="all_tilling")
    if SAVE_GIF1:
        name1 = path + "/all_tile.gif"
        bind_til_list[0].save(name1, save_all=True, append_images=bind_til_list[1:], duration=200)

    GIF_num = st.sidebar.number_input('Select a tilling number', 1, len(til_list), step=1)
    if GIF_num:
        GIF_list = til_list[GIF_num - 1]
        col2.markdown("<h1 style='text-align: center; color: black;'>Tilling image</h1>", unsafe_allow_html=True)
        col2.image(GIF_list[frame], width=200, use_column_width=True)

        SAVE_GIF2 = col2.button("SAVE GIF", key="each_tilling")
        if SAVE_GIF2:
            name2 = path + "/tile" + str(GIF_num) + '.gif'
            GIF_list[0].save(name2, save_all=True, append_images=GIF_list[1:], duration=200)
else:
    st.write("Please input folder path")