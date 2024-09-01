#CODE FOR THE CUSTOM TKINTER WINDOW
from tkinter import *
import customtkinter,openai,os,requests,re,json
from threading import Thread
import numpy as np
import PIL.Image
from pathlib import Path
import io
from icrawler.builtin import BingImageCrawler

#CLASSES


class ThemeFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0,weight=1)
        self.title_text = customtkinter.CTkLabel(master=self, text="Theme", fg_color="transparent")
        self.title_text.grid(row=0,column=0,padx=20,pady=0,sticky="ew")

        #Word Count
        self.word_text = customtkinter.CTkLabel(master=self, text="Word Count", fg_color="transparent",anchor="w")
        self.word_text.grid(row=1,column=0,padx=20,pady=0,sticky="ew")
        self.word_entry = customtkinter.CTkEntry(master=self, placeholder_text="1000")
        self.word_entry.grid(row=2,column=0,padx=30,pady=(0,10),sticky="w")

        #Style
        self.style_text = customtkinter.CTkLabel(master=self, text="Style", fg_color="transparent",anchor="w")
        self.style_text.grid(row=3,column=0,padx=20,pady=0,sticky="w")
        self.style_entry = customtkinter.CTkEntry(master=self, placeholder_text="inspire to",width=150)
        self.style_entry.grid(row=4,column=0,padx=30,pady=(0,10),sticky="w")
        self.style_text = customtkinter.CTkLabel(master=self, text="topic", fg_color="transparent",anchor="w")
        #self.style_text.grid(row=4,column=0,padx=(190,0),pady=(0,10),sticky="w")
        self.style_entry.insert(0,master.save["Theme Style"])

        #Theme
        self.theme_text = customtkinter.CTkLabel(master=self, text="Theme", fg_color="transparent",anchor="w")
        self.theme_text.grid(row=6,column=0,padx=20,pady=0,sticky="w")
        self.theme_entry=customtkinter.CTkEntry(master=self)
        self.theme_entry.grid(row=7,column=0,padx=30,pady=(0,10),sticky="ew")

        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=8,column=0,padx=(20,0),pady=(142,10),sticky="w")
        self.include_box.toggle()


class ObjectsFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0,weight=1)
        self.title_text = customtkinter.CTkLabel(master=self, text="Objects", fg_color="transparent")
        self.title_text.grid(row=0,column=0,padx=20,pady=0,sticky="ew")

        #Object Word Count
        self.word_text = customtkinter.CTkLabel(master=self, text="Objects Word Count", fg_color="transparent",anchor="w")
        self.word_text.grid(row=1,column=0,padx=20,pady=0,sticky="ew")
        self.word_entry = customtkinter.CTkEntry(master=self, placeholder_text="100")
        self.word_entry.grid(row=2,column=0,padx=30,pady=(0,10),sticky="w")

        #Style
        self.style_text = customtkinter.CTkLabel(master=self, text="Style", fg_color="transparent",anchor="w")
        self.style_text.grid(row=3,column=0,padx=20,pady=0,sticky="w")
        #self.style_text = customtkinter.CTkLabel(master=self, text="Write text that will ", fg_color="transparent",anchor="w")
        #self.style_text.grid(row=4,column=0,padx=40,pady=0,sticky="w")
        self.style_entry = customtkinter.CTkEntry(master=self, placeholder_text="describe",width=150)
        self.style_entry.grid(row=4,column=0,padx=30,pady=(0,10),sticky="w")
        self.style_text = customtkinter.CTkLabel(master=self, text="object", fg_color="transparent",anchor="w")
        #self.style_text.grid(row=4,column=0,padx=(190,0),pady=(0,10),sticky="w")
        self.style_entry.insert(0,master.save["Objects Style"])

        #Objects Input
        self.object_list_text = customtkinter.CTkLabel(master=self, text="Objects List", fg_color="transparent",anchor="w")
        self.object_list_text.grid(row=5,column=0,padx=20,pady=0,sticky="w")
        self.object_list_entry=customtkinter.CTkTextbox(master=self,height=100,border_width=2)
        self.object_list_entry.grid(row=6,column=0,padx=30,pady=0,sticky="ew")

        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=8,column=0,padx=(20,0),pady=(80,10),sticky="w")
        self.include_box.toggle()


class ImagesFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0,weight=1)
        self.title_text = customtkinter.CTkLabel(master=self, text="Images", fg_color="transparent")
        self.title_text.grid(row=0,column=0,padx=20,pady=0,sticky="ew")

        #Image Size
        self.size_text = customtkinter.CTkLabel(master=self, text="Images Resolution", fg_color="transparent",anchor="w")
        self.size_text.grid(row=1,column=0,padx=20,pady=0,sticky="ew")
        self.size_entry = customtkinter.CTkSegmentedButton(master=self, values=["256x256","512x512","1024x1024"])
        self.size_entry.grid(row=2,column=0,padx=30,pady=(0,10),sticky="ew")
        self.size_entry.set("1024x1024")
        #Images Per Object
        self.count_text = customtkinter.CTkLabel(master=self, text="Images Per Object", fg_color="transparent",anchor="w")
        self.count_text.grid(row=3,column=0,padx=20,pady=0,sticky="ew")
        self.count_entry = customtkinter.CTkSegmentedButton(master=self, values=[0,1,2,3,4])
        self.count_entry.grid(row=4,column=0,padx=30,pady=(0,10),sticky="ew")
        self.count_entry.set(2)

        #png or jpg
        self.format_text = customtkinter.CTkLabel(master=self, text="Images Format", fg_color="transparent",anchor="w")
        self.format_text.grid(row=5,column=0,padx=20,pady=0,sticky="ew")
        self.format_entry = customtkinter.CTkSegmentedButton(master=self, values=[".PNG",".JPG"])
        self.format_entry.grid(row=6,column=0,padx=30,pady=(0,10),sticky="ew")
        self.format_entry.set(".PNG")

        #image modifier
        self.mod_text = customtkinter.CTkLabel(master=self, text="Dall-E Images Modifier", fg_color="transparent",anchor="w")
        self.mod_text.grid(row=7,column=0,padx=20,pady=0,sticky="ew")
        self.mod_entry = customtkinter.CTkEntry(master=self)
        self.mod_entry.grid(row=8,column=0,padx=30,pady=(0,15),sticky="ew")
        self.mod_entry.insert(0,master.save["Images Modifier"])

        #AI Entry
        self.ai_text = customtkinter.CTkLabel(master=self, text="Image Method", fg_color="transparent",anchor="w")
        self.ai_text.grid(row=9,column=0,padx=20,pady=0,sticky="ew")
        self.ai_entry = customtkinter.CTkSegmentedButton(master=self,values=["Dall-E","Google","Pixabay","All"])
        self.ai_entry.grid(row=10,column=0,padx=30,pady=(0,15),sticky="ew")
        self.ai_entry.set("Dall-E")


        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=11,column=0,padx=(20,0),pady=(0,10),sticky="w")
        self.include_box.toggle()




class SubmitFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1)
        #Text Box
        self.textbox=customtkinter.CTkTextbox(master=self,height=60,wrap="word",state="disabled")
        self.textbox.grid(row=0,column=0,padx=20,pady=(20,10),sticky="nsew",rowspan=4)

        #API KEY
        self.key_text = customtkinter.CTkLabel(master=self, text="Open AI API Key", fg_color="transparent",anchor="w")
        self.key_text.grid(row=0,column=1,padx=20,pady=0,sticky="ew")
        self.key_entry = customtkinter.CTkEntry(master=self, placeholder_text="szk-dy63...",width=250)
        self.key_entry.grid(row=1,column=1,padx=30,pady=0,sticky="ew")
        self.key_entry.insert(0,master.save["key"])

        #Folder option
        self.folder_text = customtkinter.CTkLabel(master=self, text="Output Destination", fg_color="transparent",anchor="w")
        self.folder_text.grid(row=2,column=1,padx=20,pady=0,sticky="ew")
        self.folder_entry = customtkinter.CTkButton(master=self, text="Select Folder",command=master.select_file)
        self.folder_entry.grid(row=3,column=1,padx=30,pady=0,columnspan=1,sticky="w")

        #Selected Output Folder
        self.direc_text = customtkinter.CTkLabel(master=self, text=str("/"+master.default_path.split("\\")[-1]), fg_color="transparent",anchor="w")
        self.direc_text.grid(row=3,column=1,padx=(180,0),pady=0,sticky="w")

        #Pixa API KEY
        self.pixakey_text = customtkinter.CTkLabel(master=self, text="Pixabay API Key", fg_color="transparent",anchor="w")
        self.pixakey_text.grid(row=0,column=2,padx=20,pady=0,sticky="ew")
        self.pixakey_entry = customtkinter.CTkEntry(master=self, placeholder_text="39623...",width=250)
        self.pixakey_entry.grid(row=1,column=2,padx=30,pady=0,sticky="ew")
        self.pixakey_entry.insert(0,master.save["pixabay_key"])

        #Generate
        self.generate_button=customtkinter.CTkButton(master=self,text="Generate",command=lambda:generate(master.get()))
        self.generate_button.grid(row=3,column=2,sticky="es",padx=10,pady=10)



class StoryFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0,weight=1)
        self.title_text = customtkinter.CTkLabel(master=self, text="Story", fg_color="transparent")
        self.title_text.grid(row=0,column=0,padx=20,pady=0,sticky="ew")

        #Object Word Count
        self.word_text = customtkinter.CTkLabel(master=self, text="Word Count", fg_color="transparent",anchor="w")
        self.word_text.grid(row=1,column=0,padx=20,pady=0,sticky="ew")
        self.word_entry = customtkinter.CTkEntry(master=self, placeholder_text="100")
        self.word_entry.grid(row=2,column=0,padx=30,pady=(0,10),sticky="w")

        #Story Type
        self.type_text = customtkinter.CTkLabel(master=self, text="Story Type", fg_color="transparent",anchor="w")
        self.type_text.grid(row=3,column=0,padx=20,pady=0,sticky="ew")
        self.type_entry = customtkinter.CTkEntry(master=self, placeholder_text="Romance")
        self.type_entry.grid(row=4,column=0,padx=30,pady=(0,10),sticky="ew")

        #Story Style
        self.style_text = customtkinter.CTkLabel(master=self, text="Story Style", fg_color="transparent",anchor="w")
        self.style_text.grid(row=5,column=0,padx=20,pady=0,sticky="ew")
        self.style_entry = customtkinter.CTkEntry(master=self, placeholder_text="Gothic")
        self.style_entry.grid(row=6,column=0,padx=30,pady=(0,10),sticky="ew")


        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=11,column=0,padx=(20,0),pady=(142,10),sticky="sw")
        self.include_box.toggle()



class App(customtkinter.CTk):#MAIN APP WINDOW
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.iconbitmap("icon.ico")
        self.minsize(1200,530)
        self.resizable(False,False)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.default_path = str(Path.home() / "Downloads")
        self.path = str(self.default_path)
        self.started=False
        self.save=open_save()
        

        self.grid_rowconfigure(0,weight=3)
        self.grid_rowconfigure(1,weight=1)

        self.title(self.save["app_name"])
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0,1,2,3),weight=1)
        #self.grid_columnconfigure(1,weight=5)
        self.theme_frame=ThemeFrame(master=self)
        self.theme_frame.grid(padx=(20,10),pady=20,row=0,column=0,sticky="nsew")
        self.objects_frame=ObjectsFrame(master=self)
        self.objects_frame.grid(padx=10,pady=20,row=0,column=1,sticky="nsew")
        self.images_frame=ImagesFrame(master=self)
        self.images_frame.grid(padx=(10,10),pady=20,row=0,column=2,sticky="nsew")
        
        self.story_frame=StoryFrame(master=self)
        self.story_frame.grid(padx=(10,20),pady=20,row=0,column=3,sticky="nsew")

        self.submit_frame=SubmitFrame(master=self)
        self.submit_frame.grid(padx=(20,20),pady=(0,20),row=1,column=0,sticky="nsew",columnspan=4)

        #Progress Bar
        self.progress_bar=customtkinter.CTkProgressBar(master=self,height=20,corner_radius=0)
        self.progress_bar.grid(row=2,column=0,sticky="ew",columnspan=4)
        self.progress_bar.set(0)
        





    def get(self):
        try:
            if self.started:#Check that it's not already running
                printz("Already running!")
                return None

            #Object List
            object_list = self.objects_frame.object_list_entry.get('1.0', 'end-1c')
            object_list = re.split('[^a-zA-Z0-9 \'-]',object_list)
            print(object_list)
            for obj in range(len(object_list)):
                object_list[obj] = ''.join([i for i in object_list[obj] if not i.isdigit()]).strip()
            print(object_list)
            for obj in object_list:
                if len(obj)<2:
                    object_list.remove(obj)

            #Word Count & Object word count - NUMBER LESS THAN 3000
            word_count = self.theme_frame.word_entry.get()
            object_word_count = self.objects_frame.word_entry.get()
            story_word_count = self.story_frame.word_entry.get()

            #Only check things needed
            theme=self.theme_frame.include_box.get()
            objects=self.objects_frame.include_box.get()
            images=self.images_frame.include_box.get()
            story=self.story_frame.include_box.get()

            if len(self.submit_frame.key_entry.get())<10:
                printz("Must provide an openAI API KEY!")
                return None
            elif (not word_count.isdigit() or int(word_count)>3000) and theme==1:
                printz("Word count must not be empty and below 3000!")
                return None
            elif (len(object_list)>0 and (not object_word_count.isdigit() or int(object_word_count)>3000)) and objects==1:
                printz("Word count must not be empty and below 3000!")
                return None
            elif (len(object_list)>0 and (not story_word_count.isdigit() or int(story_word_count)>3000)) and story==1:
                printz("Word count must not be empty and below 3000!")
                return None
            elif self.theme_frame.theme_entry.get()=="":#'1.0', 'end-1c'
                printz("Theme cannot be empty!")
                return None
            elif self.theme_frame.style_entry.get()=="" and theme==1:
                printz("Theme Style cannot be empty!")
                return None
            elif self.objects_frame.style_entry.get()=="" and len(object_list)!=0 and objects==1:
                printz("Object Style cannot be empty!")
                return None


            return {
                "key":self.submit_frame.key_entry.get(),
                "pixabay_key":self.submit_frame.pixakey_entry.get(),
                "word_count":word_count,
                "object_word_count":object_word_count,
                "resolution":self.images_frame.size_entry.get(),
                "image_count":self.images_frame.count_entry.get(),
                "format":self.images_frame.format_entry.get(),
                "theme":self.theme_frame.theme_entry.get(),
                "object_list":object_list,
                "path":self.path,
                "theme_style":self.theme_frame.style_entry.get(),
                "objects_style":self.objects_frame.style_entry.get(),
                "images_style":self.images_frame.mod_entry.get(),
                "image_source":self.images_frame.ai_entry.get(),
                "theme?":theme,
                "objects?":objects,
                "images?":images,
                "story_word_count":story_word_count,
                "story_type":self.story_frame.type_entry.get(),
                "story_style":self.story_frame.style_entry.get(),
                "story?":story
            }

        except:
            printz("ERROR: Getting the inputs")
            return None

    #Opens a window to select a file
    def select_file(self):
        filename = customtkinter.filedialog.askdirectory(
            title='Select folder',
            initialdir=self.path)
        self.path=filename
        self.submit_frame.direc_text.configure(text="/"+str(filename.split("/")[-1]))





















#FUNCTIONS

#Resize image into square
def resize_image(image: Image, length: int) -> Image:
    """
    Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
    part of the image.

    :param self:
    :param image: Image to resize.
    :param length: Width and height of the output image.
    :return: Return the resized image.
    """

    """
    Resizing strategy : 
     1) We resize the smallest side to the desired dimension (e.g. 1080)
     2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
    """
    if image.size[0] < image.size[1]:
        # The image is in portrait mode. Height is bigger than width.

        # This makes the width fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))

        # Amount of pixel to lose in total on the height of the image.
        required_loss = (resized_image.size[1] - length)

        # Crop the height of the image so as to keep the center part.
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

        # We now have a length*length pixels image.
        return resized_image
    else:
        # This image is in landscape mode or already squared. The width is bigger than the heihgt.

        # This makes the height fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))

        # Amount of pixel to lose in total on the width of the image.
        required_loss = resized_image.size[0] - length

        # Crop the width of the image so as to keep 1080 pixels of the center part.
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

        # We now have a length*length pixels image.
        return resized_image
    

def open_save():# Return API key from file if possible
    if os.path.exists("save.json"):
        with open('save.json', 'r') as file:
            data = json.load(file)
        return data
    return {"key":"","Theme Style":"inspire to","Objects Style":"describe","Images Modifier":""}

def printz(string):
    app.submit_frame.textbox.configure(state="normal")
    app.submit_frame.textbox.insert(index="0.0",text=str(string)+"\n")
    app.submit_frame.textbox.configure(state="disabled")
    app.update()

#Return response from a gpt request
def ask_GPT(message):
    failed=0
    while failed<6:
        chat=None
        messages = [{"role": "user", "content": message}]
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        except Exception as e:#The Model is waiting as too many requests incoming
            printz(e)
            failed+=1
        if chat!=None:
            reply = chat.choices[0].message.content
            return reply
    return ""

############################# GENERATING WITH AI

#Generate the article txt using chatGPT
def generate_article(theme,word_count,style,path):
    message = app.save["Theme Prompt"].replace("[word_count]",str(word_count)).replace("[style]",style).replace("[theme]",theme)
    text_body = ask_GPT(message)
    text_file = path+"/"+theme+".txt"
    try:
        with open(text_file,"w") as f:
            f.write(text_body)
    except:
        printz("ERROR SAVING!")


#Generate the story txt using chatGPT
def generate_story(objs,word_count,type,style,path):
    message = app.save["Story Prompt"].replace("[word_count]",str(word_count)).replace("[style]",style).replace("[type]",type).replace("[object_list]",str(objs))
    text_body = ask_GPT(message)
    text_file = path+"/Story.txt"
    try:
        with open(text_file,"w") as f:
            f.write(text_body)
    except:
        printz("ERROR SAVING!")

#Generate each object txt using chatGPT
def generate_objects(object_list,word_count,style,path):#Gets multiple objects to process
    for obj in object_list:
        message = app.save["Object Prompt"].replace("[word_count]",str(word_count)).replace("[style]",style).replace("[object]",obj)
        text_body = ask_GPT(message)
        text_file = path+"/"+obj+".txt"
        try:
            with open(text_file,"w") as f:
                f.write(text_body)
        except:
            printz("ERROR SAVING!")

def get_google_images(object_list,image_count,format,path,key,resolution):
    if "1024" in resolution:
        resolution=1024
    elif "512" in resolution:
        resolution=512
    elif "256" in resolution:
        resolution=256
    for obj in object_list:
        prev_files = os.listdir(path)
        print(prev_files)
        google_Crawler = BingImageCrawler(storage = {'root_dir': path})
        google_Crawler.crawl(keyword = obj, max_num = image_count)
        c=0
        for file in os.listdir(path):
            if file not in prev_files:#Then is an image
                img = PIL.Image.open(path+"/"+file)
                img = resize_image(img,resolution)
                img.save(path+"/Google - "+str(obj)+str(c)+format)
                os.remove(path+"/"+file)
            c+=1

#Get object's images using PIXABAY for open source image search
def get_pixa_images(object_list,image_count,format,path,key,resolution):
    #Get Resolution
    if "1024" in resolution:
        resolution=1024
    elif "512" in resolution:
        resolution=512
    elif "256" in resolution:
        resolution=256
    
    key = key
    for obj in object_list:
        url=f'https://pixabay.com/api/?key={key}&q='+str(obj)+'&image_type=photo'
        r = requests.get(url)
        try:
            json_data = r.json()
            for image in range(image_count):
                if image < len(json_data["hits"]):
                    name = json_data["hits"][image]["id"]
                    img_url = json_data["hits"][image]["largeImageURL"]
                    r = requests.get(img_url,stream=True)
                    content = resize_image(PIL.Image.open(io.BytesIO(r.content)),resolution)
                    content.save(path+"/Pixabay - "+str(obj)+str(image)+format)
                    #with open(path+"/Google - "+str(obj)+str(image)+"."+format,"wb") as f:
                    #f.write(content)
        except:
            printz("ERROR: Issue with Pixabay key, skipping")


#Generate object's images using DALLE-2
def generate_images(object_list,resolution,image_count,format,style,path):
    for obj in object_list:
        message = obj+", "+str(style)#Sigma 85mm f.1/4 , award-winning, studio light
        response = openai.Image.create(prompt=message,n=image_count,size=resolution)#Generate Images Here
        for i in range(len(response["data"])):
            img=requests.get(response["data"][i]["url"],stream=True)
            img=PIL.Image.open(img.raw)
            if format==".PNG":
                img=img.convert("RGBA")
                img.save(path+"/DALL-E - "+str(obj)+str(i)+".png","PNG")
            else:
                img.save(path+"/DALL-E - "+str(obj)+str(i)+".jpg")
            #Save them here!


#Generate all of the object images
def generate_all_images(object_list,resolution,image_count,format,style,path):
    nthreads=30
    objs = np.array(object_list)
    objs = np.array_split(objs,nthreads)#Split data for threads
    lists=[]
    for x in objs:
        lists.append(x.tolist())
    threads = []
    for i in range(nthreads):#Create Threads
        if len(lists[i])>0:
            t = Thread(target=generate_images, args=(lists[i],resolution,image_count,format,style,path))#Split up data
            threads.append(t)
    [ t.start() for t in threads ]#Start Threads
    [ t.join() for t in threads ]#Wait for threads to complete



#Generate all of the objects 
def generate_all_objects(object_list,word_count,style,path):
    nthreads=30
    objs = np.array(object_list)
    objs = np.array_split(objs,nthreads)#Split data for threads
    lists=[]
    for x in objs:
        lists.append(x.tolist())
    threads = []
    for i in range(nthreads):#Create Threads
        if len(lists[i])>0:
            t = Thread(target=generate_objects, args=(lists[i],word_count,style,path))#Split up data
            threads.append(t)
    [ t.start() for t in threads ]#Start Threads
    [ t.join() for t in threads ]#Wait for threads to complete


def generate(data):
    Thread(target=API_call,args=(data,)).start()


###################### MAIN API CALL FUNCTION


#This initialises openAI API and creates new folder 
def API_call(data):
    try:
        if data==None:
            return

        # Connect to the API
        openai.api_key=data["key"]#FIX BAD KEY!
        # Create Filepath
        path = os.path.join(data["path"],data["theme"])
        #Check if already created!!
        if not os.path.exists(path):#IF the path does not exist, then create it!
            os.mkdir(path)

        if not os.path.exists(path):
            printz("No file permission")
            return

        printz("Generation started...")
        app.started=True
        #1. Create new folder
        printz("1. Getting folder")
        
        app.progress_bar.set(0.2)
        #2. Generate article
        if data["theme?"]:
            printz("2. Generating Article")
            generate_article(data["theme"],data["word_count"],data["theme_style"],path)
        else:
            printz("2. Skipped Article")
        app.progress_bar.set(0.4)

        #3. Generate Objects
        if data["objects?"]:
            printz("3. Generating Objects")
            generate_all_objects(data["object_list"],data["object_word_count"],data["objects_style"],path)
        else:
            printz("3. Skipped Objects")
        app.progress_bar.set(0.6)

        #4. Generate Images
        if data["images?"]:
            if data["image_count"]!=0:
                printz("4. Generating Images")
                if data["image_source"]=="Dall-E" or data["image_source"]=="All":
                    generate_all_images(data["object_list"],data["resolution"],data["image_count"],data["format"],data["images_style"],path)
                if data["image_source"]=="Pixabay" or data["image_source"]=="All":
                    get_pixa_images(data["object_list"],data["image_count"],data["format"],path,data["pixabay_key"],data["resolution"])
                if data["image_source"]=="Google" or data["image_source"]=="All":
                    get_google_images(data["object_list"],data["image_count"],data["format"],path,data["pixabay_key"],data["resolution"]) 
        else:
            printz("4. Skipped Images")
        app.progress_bar.set(0.8)

        #5. Generate Story
        if data["story?"]:
            printz("5. Generating Story")
            generate_story(data["object_list"],data["story_word_count"],data["story_type"],data["story_style"],path)
        else:
            printz("5. Skipped Story")
        printz("Completed!")
        app.progress_bar.set(1)
        app.started=False


    except Exception as e:
        print(e)
        printz("ERROR: Generating the files")
        app.started=False
        app.progress_bar.set(0)



if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    if os.path.exists("theme.json"):
        customtkinter.set_default_color_theme("theme.json")
    app=App()
    app.mainloop()

