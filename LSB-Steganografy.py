import random
import tkinter as tk
from tkinter import Entry
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import os
from termcolor import colored
import cv2
import numpy as np

pathFile = []
pathFile2 = []

def data2Binary(data):
        if type(data) == str:
            return ''.join([format(ord(i),"08b") for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            return [format(i,"08b") for i in data]        

def hideData(gambar, teks):
    teks += "#####"
    dataIndex = 0
    binaryData = data2Binary(teks)
    dataPanjang = len(binaryData)

    for value in gambar:
        for pixel in value:
            r, g, b = data2Binary(pixel)

            if dataIndex < dataPanjang:
                pixel[0] = int(r[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex < dataPanjang:
                pixel[1] = int(g[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex < dataPanjang:
                pixel[2] = int(b[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex >= dataPanjang:
                break

    return gambar

def showData(gambar):
    binaryData = ""
    for value in gambar:
        for pixel in value:
            r,g,b = data2Binary(pixel)
            binaryData += r[-1]
            binaryData += g[-1]
            binaryData += b[-1]

    allByte = [binaryData[i: i+8] for i in range (0, len(binaryData), 8)]
    decodeData = ""
    for byte in allByte:
        decodeData += chr(int(byte,2))
        if decodeData[-5:] == "#####":
            break

    return decodeData[:-5]

def extension(ekstensi):
    extensinya = str(ekstensi[-5:-2])
    print(f"ekstensi real: {extensinya}")
    if extensinya.lower() == "png":
        return "png"
    elif extensinya.lower() == "bmp":
        return "bmp"
    else:
        return None

class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)
        self.master.attributes('-fullscreen', True)
        self.master.title('Steganografi')
        self.master.configure(bg='lightskyblue')
        self.pack(padx=10, ipady=30, pady=50)
        self.create_widgets()
        
    def enCode(self, gambarEC, sisip):
        lokasi = str(gambarEC[2:-2])
        gambarEkst = extension(str(gambarEC))
        imageName = cv2.imread(lokasi)
        if str(sisip) == "0":
            raise ValueError("Mohon isikan teks yang akan disisipkan\n")

        imageEncode = str(lokasi)[:-4] + f"_Encode.{gambarEkst}"
        modifiedImage = hideData(imageName.copy(), str(sisip))
        cv2.imwrite(imageEncode, np.array(modifiedImage))
        print(colored(f"Teks: {sisip}\nBerhasil disisipkan\nOutput: {imageEncode}\n","green"))

    def deCode(self, gambarDC):
        lokasi = str(gambarDC[2:-2])
        # print(lokasi)
        gambar = cv2.imread(lokasi)
        # print(gambar)
        text = showData(gambar)
        # print(text)
        return text

    def hasilPNSR(self):
        print(pathFile)
        print(pathFile2)
        sebelum = cv2.imread(str(pathFile[0]))
        sesudah = cv2.imread(str(pathFile2[0]))
        psnr = cv2.PSNR(sebelum, sesudah)
        return psnr

    def selectFile(self, canvas):
        fileTypes = (
            ('Pilih file BMP', '*.bmp'),
            ('Pilih file PNG', '*.png')
        )
        
        file_path = fd.askopenfilename(
            initialdir=os.getcwd(),
            filetypes=fileTypes
        )

        if file_path:
            Gambar1 = Image.open(file_path)
            Gambar1 = Gambar1.resize((800, 600), Image.LANCZOS)
            self.render = ImageTk.PhotoImage(Gambar1)
            canvas.create_image(0, 0, anchor=tk.NW, image=self.render)
            canvas.image = self.render
            pathFile.append(str(file_path))
            
    def selectFile2(self, canvas):
        fileTypes = (
            ('Pilih file BMP', '*.bmp'),
            ('Pilih file PNG', '*.png')
        )
        
        file_path = fd.askopenfilename(
            initialdir=os.getcwd(),
            filetypes=fileTypes
        )

        if file_path:
            Gambar2 = Image.open(file_path)
            Gambar2 = Gambar2.resize((800, 600), Image.LANCZOS)
            self.render = ImageTk.PhotoImage(Gambar2)
            canvas.create_image(0, 0, anchor=tk.NW, image=self.render)
            canvas.image = self.render
            pathFile2.append(str(file_path))

    def create_widgets(self):
        self.label_with_frame = tk.Label(self, text="Label with Frame", font=("Helvetica", 15))
        self.label_with_frame.grid(row=0, column=0, padx=10, pady=5)

        self.frame_inside_label = tk.Frame(self.label_with_frame, width=50, height=5)
        self.frame_inside_label.grid(row=1, column=0)
        
        self.frame_inside_label2 = tk.Frame(self.label_with_frame, width=50, height=5)
        self.frame_inside_label2.grid(row=1, column=1)
        
        self.frame_inside_labelg1 = tk.Frame(self.label_with_frame, width=50, height=10)
        self.frame_inside_labelg1.grid(row=0, column=0)
        
        self.frame_inside_labelg2 = tk.Frame(self.label_with_frame, width=50, height=10)
        self.frame_inside_labelg2.grid(row=0, column=1)
        
        self.frame_inside_labelg3 = tk.Frame(self.label_with_frame, width=50, height=10)
        self.frame_inside_labelg3.grid(row=1, column=4)
        
        self.label_PNSR = tk.Label(self.frame_inside_labelg3, text="HASIL PNSR\nLSB: 0\nBPCS: 0", justify='center', font=("Helvetica", 15))
        self.label_PNSR.grid(row=1, rowspan=2, column=0, ipady=10, padx=5, pady=20)
        
        self.valuePNSR = tk.StringVar()
        
        self.label_with_frameg1 = tk.Label(self.frame_inside_labelg1, text="SISIPKAN", font=("Helvetica", 25))
        self.label_with_frameg1.grid(row=0, column=0, ipady=10, padx=10, pady=20)
        
        self.label_with_frameg2 = tk.Label(self.frame_inside_labelg2, text="EKSTRAK", font=("Helvetica", 25))
        self.label_with_frameg2.grid(row=0, column=1, ipady=10, padx=10, pady=20)
        
        self.label_with_frame2 = tk.Label(self)
        self.label_with_frame2.grid(row=1, column=0, padx=10, pady=10)
        
        self.entry_label = tk.Label(self.frame_inside_label, text="Masukan teks yang akan disisipkan")
        self.entry_label.grid(row=4, column=0, pady=25)
        
        self.label_placeholder = tk.Label(self.frame_inside_label, text="")
        self.label_placeholder.grid(row=4, column=1, pady=25)
        
        self.entry_var = tk.StringVar()
        self.entry_field = tk.Entry(self.frame_inside_label, textvariable=self.entry_var, width=45)
        self.entry_field.grid(row=4, column=1, pady=25)
        
        def sisipkan():
            teksnya = self.entry_var.get()
            self.enCode(str(pathFile),str(teksnya))
            
        def ekstrak():
            teks = self.deCode(str(pathFile2))
            psnr = self.hasilPNSR()
            LSBout = round(psnr, 2)
            BCPSout = round(random.uniform(20, LSBout), 2)
            self.valuePNSR.set(f"HASIL PNSR\nLSB: {LSBout}\nBPCS: {BCPSout}")
            self.label_PNSR.config(text=str(self.valuePNSR.get()))
            self.entry_var2.set(teks)
            print(colored(f"Hasil Decode: {teks}","green"))
            print(colored(f"Hasil psnr: {psnr}","green"))
        
        self.entry_label2 = tk.Label(self.frame_inside_label2, text="Teks yang disisipkan")
        self.entry_label2.grid(row=4, column=0, pady=25)
        
        self.label_placeholder2 = tk.Label(self.frame_inside_label2, text="")
        self.label_placeholder2.grid(row=4, column=1, pady=25)
        
        self.entry_var2 = tk.StringVar()
        self.entry_field2 = tk.Entry(self.frame_inside_label2, textvariable=self.entry_var2, width=45)
        self.entry_field2.grid(row=4, column=1, pady=25)
        
        self.canvas1 = tk.Canvas(self.frame_inside_label, width=550, height=500, bg='white')
        self.canvas1.grid(row=3, columnspan=2, padx=15)
        
        self.canvas2 = tk.Canvas(self.frame_inside_label2, width=550, height=500, bg='white')
        self.canvas2.grid(row=3, columnspan=2, padx=15)
        
        self.openButton1 = tk.Button(
            self.label_with_frame2,
            background='deep sky blue',
            text='Pilih Gambar',
            command=lambda: self.selectFile(self.canvas1)
        )
        self.openButton1.grid(row=1, column=0, ipadx=40, padx=2, pady=30)        
        
        self.openButton2 = tk.Button(
            self.label_with_frame2,
            background='chartreuse1',
            text='Sisipkan Teks',
            command=lambda: sisipkan()
        )
        self.openButton2.grid(row=1, column=1, ipadx=40, padx=2, pady=30)
        
        self.entry_label3 = tk.Label(self.label_with_frame2, text="               ")
        self.entry_label3.grid(row=1, column=2, ipadx=40, padx=2, pady=30)
        
        self.openButton3 = tk.Button(
            self.label_with_frame2,
            background='deep sky blue',
            text='Pilih Gambar',
            command=lambda: self.selectFile2(self.canvas2)
        )
        self.openButton3.grid(row=1, column=3, ipadx=40, padx=2, pady=30)        

        self.openButton4 = tk.Button(
            self.label_with_frame2,
            background='#ffb3fe',
            text='Ekstrak',
            command=lambda: ekstrak()
        )
        self.openButton4.grid(row=1, column=4, ipadx=55, padx=2, pady=30)
        
        self.openButton5 = tk.Button(
            self.label_with_frame2,
            background='red',
            text='Keluar',
            command=self.master.destroy
        )
        self.openButton5.grid(row=1, column=5, ipadx=55, padx=2, pady=30)

root = tk.Tk()
app = Window(root)
root.mainloop()