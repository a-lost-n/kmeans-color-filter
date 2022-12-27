import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import requests
from io import BytesIO
import time

class filterModel():
    def __init__(self):
        self.num_tones = 3
        self.intensity = 0.7
        self.stored_image = Image.open('resources/doda.jpg')
        self.__set_color((128,128,128))
        self.filter()

    def __set_color(self, color):
        self.color_v = np.array(color)/256

    def __find_labels(self):
        if not hasattr(self, 'stored_image'):
            raise Exception("No image has been loaded yet. Use method load_image() to load an image first.")
        img = np.array(self.stored_image)
        flat_img = img.reshape((img.shape[0]*img.shape[1], 3))

        clf = KMeans(n_clusters=self.num_tones, n_init=1, tol=1e-4).fit(flat_img)

        # reduced_img = np.unique(flat_img, axis=0)
        # clf = KMeans(n_clusters=self.num_tones, n_init=1, tol=1e-4).fit(reduced_img)
        # self.dict = np.full((256,256,256), -1)
        # for pix, label in zip(reduced_img, clf.labels_):
        #     self.dict[pix[0]][pix[1]][pix[2]] = label
        # self.ga = np.array([self.dict[pix[0]][pix[1]][pix[2]] for pix in flat_img])

        self.labels = clf.labels_
        self.centers = clf.cluster_centers_

    def __add_filter(self):
        if (not hasattr(self, 'labels')) or (not hasattr(self, 'centers')):
            raise Exception("Labels haven't been found yet. Use method [REDACTED] to find the labels.")
        if self.intensity == 0:
            new_img = self.centers[self.labels]
        else:
            mean_color_map = (self.centers*np.array([0.3,0.59,0.11])).sum(axis=1)
            mcm = np.hstack((np.array([mean_color_map]).T, np.array([np.arange(self.num_tones)]).T)).astype(np.uint8)
            mcm = mcm[(mcm[:, 0]).argsort()]
            new_labels = np.hstack((np.array([(mcm.T)[1]]).T, np.array([np.arange(self.num_tones)]).T)).astype(np.uint8)
            new_labels = ((new_labels[(new_labels[:, 0]).argsort()]).T)[1]

            color_scale = np.zeros((self.num_tones, 3))
            div = self.num_tones + 1
            for i in range(div-1):
                clr = int(511*(i+1)/div) 
                if clr < 256:
                    color_scale[i] = self.color_v*clr
                else:
                    color_scale[i] = self.color_v*255 + (np.array([1,1,1]) - self.color_v) * (clr - 256)

            new_img = self.centers[self.labels]*(1-self.intensity) + color_scale[new_labels[self.labels]]*self.intensity
            # new_img = self.centers[self.ga]*(1-self.intensity) + color_scale[new_labels[self.ga]]*self.intensity
        self.last_processed_image = Image.fromarray(new_img.reshape(np.array(self.stored_image).shape).astype(np.uint8)).convert('RGB')
    
    def update_num_tones(self, updt):
        # t0 = time.time()
        self.num_tones = updt
        self.__find_labels()
        self.__add_filter()
        # t1 = time.time()
        # print("Tones: {}, Time: {}s".format(updt,t1-t0))

    def update_color(self, updt):
        self.__set_color(updt)
        self.__add_filter()

    def update_intensity(self, updt):
        self.intensity = updt
        self.__add_filter()

    def filter(self):
        if not hasattr(self, 'stored_image'):
            raise Exception("No image has been loaded yet. Use method load_image() to load an image first.")
        self.__find_labels()
        self.__add_filter()
    
    def load_image(self, route):
        self.stored_image = Image.open(route)
        self.filter()

    def import_image(self, url):
        self.stored_image = np.array(Image.open(BytesIO(requests.get(url).content)).convert('RGB'))
        self.filter()       

    def save_image(self, route):
        self.last_processed_image.save(route)

    def display(self):
        if not hasattr(self, 'last_processed_image'):
            raise Exception("No image has been processed yet. Use method filter() to process an image first.")
        self.last_processed_image.show()

    def get_image(self):
        if not hasattr(self, 'last_processed_image'):
            raise Exception("No image has been processed yet. Use method filter() to process an image first.")
        return self.last_processed_image

    def expanded_image(self):
        # Image has to fit in a 720x720 space. If bigger, longest dimension has to resize to 720, else ignore
        grid_dim = 720
        background = Image.fromarray(np.zeros([grid_dim, grid_dim, 3], dtype=np.uint8))
        img = self.last_processed_image
        x_dim = img.size[0]
        y_dim = img.size[1]
        l_dim = max(x_dim, y_dim, grid_dim)
        if l_dim > grid_dim:
            x_dim = int(grid_dim*x_dim/l_dim)
            y_dim = int(grid_dim*y_dim/l_dim)
            img = img.resize((x_dim, y_dim))
        mid_point_x = int((grid_dim-x_dim)/2)
        mid_point_y = int((grid_dim-y_dim)/2)
        background.paste(img, (mid_point_x, mid_point_y))
        return background
    
         