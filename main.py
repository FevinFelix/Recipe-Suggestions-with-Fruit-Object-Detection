#%%
import tkinter # to get this to import in a virtual environment, do "brew install python-tk@3.10 to match your python version"
import customtkinter
from PIL import Image
import requests
from io import BytesIO
from tkinter import filedialog
import math

import ultralytics
from ultralytics import YOLO

import os
import shutil

from API_Retrieve import get_recipes
from RecipeFrame import RecipeFrame

model = YOLO("best7.pt")

def return_detected(imgPath) -> list:
    results = model.predict(source=imgPath, save=True)  # predict on an image
    classes = {
        0 : "apples",
        1 : "bananas",
        2 : "grapes",
        3 : "oranges",
        4 : "strawberries"
    }

    converted = results[0].boxes.cls.cpu().numpy() # converts the tensor array to a list
    detected = []

    for number in converted:  #used class names to 
        if classes[number] not in detected:
            detected.append(classes[number])
    return detected


class recipe():

     def __init__(self, picture, link, name, missed_ingredients):
         self.picture = picture
         self.link = link
         self.name = name
         self.missed_ingredients = missed_ingredients
#%%

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title("small example app")
        self.minsize(300, 200)

        # create grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=4, padx=0, pady=(0, 0), sticky="nesw")

        self.upload_button = customtkinter.CTkButton(master=self, command=self.upload_and_display, text="Upload Image")
        self.upload_button.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.recipe_button = customtkinter.CTkButton(master=self, command=self.display_recipe, text="Show Recipes")
        self.recipe_button.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.next_button = customtkinter.CTkButton(master=self, text="Next Recipe")
        self.next_button.grid(row=1, column=2, padx=10, pady=10, sticky="we")
        self.previous_button = customtkinter.CTkButton(master=self, text="Previous Recipe")
        self.previous_button.grid(row=1, column=3, padx=10, pady=10, sticky="we")

        self.detected_fruits = []
        self.has_textbox = True

    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")
    
    def upload_and_display(self):
        if (self.has_textbox):
            self.textbox.destroy()

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.has_textbox = True
        self.textbox.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 0), sticky="nesw")
        text = self.textbox

        your_Image=filedialog.askopenfilename(title = "Select your image",filetypes = [("Image Files","*.png"),("Image Files","*.jpg")])
        img_File=Image.open(your_Image)
        
        # runs object detection on image and retrieves converted image
        results = model.predict(source=img_File.filename, save=True) 
        head, tail = os.path.split(img_File.filename)
        print(tail)
        converted_img = Image.open(f"./runs/detect/predict/{tail}")

        # also retrieves the detected fruit names in a list
        self.detected_fruits = return_detected(img_File)

        # finds maximum image dimensions
        original_h = img_File.height
        original_w = img_File.width
        target_area = (text.winfo_height())* (text.winfo_width())
        new_w = math.sqrt((original_w / original_h) * target_area)
        new_h = target_area / new_w

        if (new_h > new_w):
            new_h /= 1.5
            new_w /= 1.5
        else:
            new_h /= 1.1
            new_w /= 1.1 

        your_image = customtkinter.CTkImage(light_image=converted_img, size=(new_w, new_h))
        label = customtkinter.CTkLabel(master=text, image=your_image, text='')
        label.grid(column=0, row=0, columnspan=4)

    def display_recipe(self):
        self.textbox.destroy()
        self.has_textbox = False

        recipes = get_recipes(self.detected_fruits)
        picture = recipes[6].picture
        recipe_name = recipes[6].name
        recipe_link = recipes[6].link
        missed = recipes[6].missed_ingredients

        self.recipe_frame = RecipeFrame(self, image = picture, name = recipe_name, link = recipe_link, missed_ingredients = missed)
        self.recipe_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="nesw")



app = App()

# removes files from previous runs
try:
    shutil.rmtree("./runs", ignore_errors=True)
except:
    print("Clean slate")

app.mainloop()
