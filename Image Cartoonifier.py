import os
import sys
import tkinter as tk
from tkinter import *

import cv2  # Image Processing
import easygui  # Filebox
import matplotlib.pyplot as plt

mainContainer = tk.Tk()
mainContainer.geometry('300x300')
mainContainer.title('Image Cartoonist')
mainContainer.configure(background='LightYellow')

# Image Size |> Fixed
W = 960  # Width
H = 540  # Height


def uploadImage():
    imgPath = easygui.fileopenbox()
    Cartoonify(imgPath)


def Cartoonify(imgPath):
    origImg = cv2.imread(imgPath)  # Read the Image
    origImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2RGB)
    # print(origImg)  # Image read in form of numbers

    if origImg is None:  # Check valid image
        print("Can't find any image, Please choose valid one..")
        sys.exit()

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

    fig, axes = plt.subplots(
        3, 2,  # 3 rows, 2 cols
        figsize=(8, 8),
        subplot_kw={'xticks': [], 'yticks': []},
        gridspec_kw=dict(hspace=0.1, wspace=0.1),
    )

    for i, ax in enumerate(axes.flat):
        ax.set_title('fig(' + str(1 + i) + ')')
        ax.imshow(images[i], cmap='gray')

    saveImgBtn = Button(
        mainContainer,
        text="Save |> Cartooned Image",
        command=lambda: saveImage(ReSized6, imgPath),
        padx=15, pady=5,
        background='Black', foreground='Gold',
        font=('Calibri', 16, 'bold')
    )
    saveImgBtn.pack(side=TOP, pady=5)

    plt.show()


def saveImage(ReSized6, imgPath):
    newName = "Cartooned Image"
    path = os.path.dirname(imgPath)
    extension = os.path.splitext(imgPath)[1]  # get Extension of the Image
    imgIdentity = os.path.join(path, (newName + extension))  # join the Full Image Identifier
    cv2.imwrite(imgIdentity, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    tk.messagebox.showinfo(
        title='Save The Cartoonified Image',
        message=("Saved |> " + newName + extension + " |> " + path)
    )


########################################################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # Main # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
metaData = Label(
    mainContainer,
    text="Image Cartoonifier\n\nBy:\nAhmed Nasser\n_________________________",
    padx=15, pady=5,
    background='Snow', foreground='Red',
    font=('Georgia', 12, 'bold')
)
metaData.pack(side=TOP, pady=5)

uploadImgBtn = Button(
    mainContainer,
    text="Cartoonify |> Choose Image",
    command=uploadImage,
    padx=15, pady=5,
    background='Black', foreground='LawnGreen',
    font=('Calibri', 15, 'bold')
)
uploadImgBtn.pack(side=TOP, pady=25)

mainContainer.mainloop()
########################################################################################################################
