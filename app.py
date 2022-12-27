import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, askopenfilename
from PIL import ImageTk
from model import *
         

class App():

    def __init__(self):
        self.filetypes = [('JPG Image', '*.jpg')]
        self.fm = filterModel()
        self.root = tk.Tk()
        self.root.geometry('1080x720')
        self.root.resizable(False, False)
        self.root.title('KMC Filter')
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        img = ImageTk.PhotoImage(self.fm.expanded_image())

        self.display_img = tk.Label(self.root,image=img)
        self.display_img.pack(side=tk.LEFT)

        self.ctrl = {}

        self.ctrl['num_layers_label'] = tk.Label(self.root,text="Number of Tones")
        self.ctrl['num_layers_slider'] = tk.Scale(self.root,from_=2,to=32,resolution=1,orient="horizontal")
        self.ctrl['num_layers_slider'].bind("<ButtonRelease-1>",self.update_tones)
        self.ctrl['num_layers_slider'].set(self.fm.num_tones)

        self.ctrl['color_label'] = tk.Label(self.root,text="Color")
        self.ctrl['color_button'] = tk.Button(self.root,text="Choose color",command=self.change_color)

        self.ctrl['intensity_label'] = tk.Label(self.root,text="Intensity")
        self.ctrl['intensity_slider'] = tk.Scale(self.root,from_=0,to=1,resolution=0.01,orient="horizontal")
        self.ctrl['intensity_slider'].bind("<ButtonRelease-1>",self.update_intensity)
        self.ctrl['intensity_slider'].set(self.fm.intensity)

        self.ctrl['load_button'] = tk.Button(self.root,text="Load Image",command=self.load)
        self.ctrl['import_button'] = tk.Button(self.root,text="Import Image",command=self.import_url)
        self.ctrl['save_button'] = tk.Button(self.root,text="Save Image",command=self.save)

        for item in self.ctrl.values():
            item.pack(anchor=tk.W, expand=True, padx=5, fill=tk.X)

        self.root.mainloop()

    def __refresh_image(self):
        img = ImageTk.PhotoImage(self.fm.expanded_image())
        self.display_img.configure(image=img)
        self.display_img.image = img

    def change_color(self):
        try:
            colors = askcolor(title="Tkinter Color Chooser")
            self.fm.update_color(colors[0])
            self.__refresh_image()
        except Exception:
            pass

    def update_tones(self, event):
        self.fm.update_num_tones(self.ctrl['num_layers_slider'].get())
        self.__refresh_image()

    def update_intensity(self, event):
        self.fm.update_intensity(self.ctrl['intensity_slider'].get())
        self.__refresh_image()

    def load(self):
        try:
            filename = askopenfilename(title='Open a file',filetypes=self.filetypes,defaultextension=self.filetypes)
            self.fm.load_image(filename)
            self.__refresh_image()
        except Exception:
            pass

    def save(self):
        try:
            filename = asksaveasfile(filetypes=self.filetypes,defaultextension=self.filetypes)
            self.fm.save_image(filename)
        except Exception:
            pass

    def close_popout(self):
        try:
            self.url_image = self.fm.import_image(self.url_entry.get())
            self.__refresh_image()
        except Exception:
            pass
        finally:
            self.popout.destroy()

    def import_url(self):
        self.popout = tk.Toplevel(self.root)
        self.popout.geometry("480x120")
        tk.Label(self.popout,text="Pega el url de una imagen").pack(expand=True, padx=5, fill=tk.X)
        self.url_entry = tk.Entry(self.popout)
        self.url_entry.pack(expand=True, padx=5, fill=tk.X)
        tk.Button(self.popout,text='Ok',command=self.close_popout).pack(expand=True, ipadx=5)


if __name__ == '__main__':
    app = App()
