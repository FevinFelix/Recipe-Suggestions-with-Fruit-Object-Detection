import customtkinter
import requests
from PIL import Image
from io import BytesIO
import math

class RecipeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, image, name, link, missed_ingredients, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox1 = customtkinter.CTkTextbox(master=self)
        self.textbox1.configure(state="disabled")  # configure textbox to be read-only
        self.textbox1.grid(row=0, column=0, columnspan=1, padx=(0,5), pady=(0, 0), sticky="nesw")
        
        self.textbox2 = customtkinter.CTkTextbox(master=self, font = ("Times New Roman", 25))
        #self.textbox2.configure(state="disabled")  # configure textbox to be read-only
        self.textbox2._set_dimensions(400, 500)
        self.textbox2.grid(row=0, column=1, columnspan=1, padx=(5,0), pady=(0, 0), sticky="nesw")

        # convert missed ingredients list into printable format
        missing_ingredients = ""
        for ingredient in missed_ingredients:
            missing_ingredients += (ingredient + '\n')

        # get the picture
        response = requests.get(image)
        img = Image.open(BytesIO(response.content))

        # size the picture correctly
        original_h = img.height
        original_w = img.width
        target_area = (self.textbox1.winfo_height()) * (self.textbox1.winfo_width())
        new_w = math.sqrt((original_w / original_h) * target_area)
        new_h = target_area / new_w
        # put the picture into the left textbox (multiply by 800 to fix scaling issue)
        your_image = customtkinter.CTkImage(light_image=img, size=(new_w * 800, new_h * 800))

        label = customtkinter.CTkLabel(master=self.textbox1, image=your_image, text='')
        label.grid(column=0, row=0, columnspan=1)

        # insert the name, link, and missed ingredients of the dish into the right textbox
        self.textbox2.insert(0.0, "Missing Ingredients:" + '\n' + missing_ingredients)
        self.textbox2.insert(0.0, "Link:" + '\n' + link + '\n'*2)
        self.textbox2.insert(0.0, "Name: " + name + '\n'*2)

