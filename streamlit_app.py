import cv2
import easygui
import streamlit as st
import matplotlib.pyplot as plt

# Image Size |> Fixed
W = 960  # Width -> 960
H = 540  # Height -> 540

def uploadImage():
    imgPath = easygui.fileopenbox()
    Cartoonify(imgPath)

def Cartoonify(imgPath):
    origImg = cv2.imread(imgPath)  # Read the Image
    origImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2RGB)

    if origImg is None:  # Check valid image
        st.error("Can't find any image. Please choose a valid one.")
        return

    ReSized1 = cv2.resize(origImg, (W, H))  # 1st Image (Original)

    # Conversion to Grayscale
    grayScaleImage = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (W, H))  # 2nd image

    # Blur to Smoothen the Image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (W, H))  # 3rd Image

    # Try to get the edges of the image, by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (W, H))  # 4th image

    # Applying Bilateral |> Remove Noise and Sharpen the Edges
    colorImage = cv2.bilateralFilter(origImg, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (W, H))  # 5th Image

    # Applying the Mask of Edged Image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (W, H))  # 6th Image

    # Plotting whole Images
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    for i, image in enumerate(images):
        st.subheader(f"fig({i+1})")
        st.image(image, use_column_width=True, caption=f"Figure {i+1}")

    if st.button("Save |> Cartooned Image"):
        saveImage(ReSized6, imgPath)

def saveImage(ReSized6, imgPath):
    newName = "Cartooned_Image"
    path = os.path.dirname(imgPath)
    extension = os.path.splitext(imgPath)[1]  # get Extension of the Image
    imgIdentity = os.path.join(path, (newName + extension))  # join the Full Image Identifier
    cv2.imwrite(imgIdentity, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    st.success(f"Saved as {newName}{extension} in {path}")

# Main
st.title("Image Cartoonifier")
st.markdown("By: Ahmed Nasser")

uploadImgBtn = st.button("Cartoonify |> Choose Image")
if uploadImgBtn:
    uploadImage()
