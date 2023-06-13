import cv2
import streamlit as st
import matplotlib.pyplot as plt

W = 960  # Width -> 960
H = 540  # Height -> 540


def cartoonify_image(img_path):
    orig_img = cv2.imread(img_path)
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)

    if orig_img is None:
        st.error("Can't find any image. Please choose a valid one.")
        return

    resized1 = cv2.resize(orig_img, (W, H))

    gray_scale_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(gray_scale_img, (W, H))

    smooth_gray_scale = cv2.medianBlur(gray_scale_img, 5)
    resized3 = cv2.resize(smooth_gray_scale, (W, H))

    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    resized4 = cv2.resize(get_edge, (W, H))

    color_image = cv2.bilateralFilter(orig_img, 9, 300, 300)
    resized5 = cv2.resize(color_image, (W, H))

    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    resized6 = cv2.resize(cartoon_image, (W, H))

    images = [resized1, resized2, resized3, resized4, resized5, resized6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))

    for i, ax in enumerate(axes.flat):
        ax.set_title('fig(' + str(1 + i) + ')')
        ax.imshow(images[i], cmap='gray')

    st.pyplot(fig)

    if st.button("Save |> Cartooned Image"):
        save_image(resized6, img_path)


def save_image(resized_img, img_path):
    new_name = "Cartooned Image"
    path = os.path.dirname(img_path)
    extension = os.path.splitext(img_path)[1]
    img_identity = os.path.join(path, (new_name + extension))
    cv2.imwrite(img_identity, cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))
    st.success("Saved |> " + new_name + extension + " |> " + path)


def main():
    st.title("Image Cartoonist")
    st.markdown("By:\nAhmed Nasser\n_________________________")

    uploaded_file = st.file_uploader("Cartoonify |> Choose Image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        img_path = "./temp_img." + uploaded_file.name.split(".")[-1]
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        cartoonify_image(img_path)


if __name__ == "__main__":
    main()
