#CODE FOR THE CUSTOM TKINTER WINDOW
from tkinter import *
import customtkinter,openai,os,requests,re,json
from threading import Thread
import numpy as np
import PIL.Image


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
        self.style_text.grid(row=4,column=0,padx=(190,0),pady=(0,10),sticky="w")
        self.style_entry.insert(0,master.save["Theme Style"])

        #Theme
        self.theme_text = customtkinter.CTkLabel(master=self, text="Theme", fg_color="transparent",anchor="w")
        self.theme_text.grid(row=6,column=0,padx=20,pady=0,sticky="w")
        self.theme_entry=customtkinter.CTkEntry(master=self)
        self.theme_entry.grid(row=7,column=0,padx=30,pady=(0,10),sticky="ew")

        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=8,column=0,padx=(20,0),pady=(70,10),sticky="w")
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
        self.style_text.grid(row=4,column=0,padx=(190,0),pady=(0,10),sticky="w")
        self.style_entry.insert(0,master.save["Objects Style"])

        #Objects Input
        self.object_list_text = customtkinter.CTkLabel(master=self, text="Objects List", fg_color="transparent",anchor="w")
        self.object_list_text.grid(row=5,column=0,padx=20,pady=0,sticky="w")
        self.object_list_entry=customtkinter.CTkTextbox(master=self,height=100)
        self.object_list_entry.grid(row=6,column=0,padx=30,pady=0,sticky="ew")

        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=8,column=0,padx=(20,0),pady=(10,10),sticky="w")
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
        self.mod_text = customtkinter.CTkLabel(master=self, text="Images Modifier", fg_color="transparent",anchor="w")
        self.mod_text.grid(row=7,column=0,padx=20,pady=0,sticky="ew")
        self.mod_entry = customtkinter.CTkEntry(master=self)
        self.mod_entry.grid(row=8,column=0,padx=30,pady=(0,15),sticky="ew")
        self.mod_entry.insert(0,master.save["Images Modifier"])

        #Include
        self.include_box = customtkinter.CTkCheckBox(master=self,text="Include")
        self.include_box.grid(row=9,column=0,padx=(20,0),pady=(0,10),sticky="w")
        self.include_box.toggle()


class SubmitFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1)
        #Text Box
        self.textbox=customtkinter.CTkTextbox(master=self,height=60,wrap="word",state="disabled")
        self.textbox.grid(row=0,column=0,padx=20,pady=(20,10),sticky="nsew",rowspan=4)

        #API KEY
        self.key_text = customtkinter.CTkLabel(master=self, text="API Key", fg_color="transparent",anchor="w")
        self.key_text.grid(row=0,column=1,padx=20,pady=0,sticky="ew")
        self.key_entry = customtkinter.CTkEntry(master=self, placeholder_text="szk-dy63...")
        self.key_entry.grid(row=1,column=1,padx=30,pady=0,sticky="ew")
        self.key_entry.insert(0,master.save["key"])

        #Folder option
        self.folder_text = customtkinter.CTkLabel(master=self, text="Output Destination", fg_color="transparent",anchor="w")
        self.folder_text.grid(row=2,column=1,padx=20,pady=0,sticky="ew")
        self.folder_entry = customtkinter.CTkButton(master=self, text="Select Folder",command=master.select_file)
        self.folder_entry.grid(row=3,column=1,padx=30,pady=0,columnspan=1,sticky="w")

        #Selected Output Folder
        self.direc_text = customtkinter.CTkLabel(master=self, text="Default", fg_color="transparent",anchor="w")
        self.direc_text.grid(row=3,column=1,padx=(180,0),pady=0,sticky="w")


        #Generate
        self.generate_button=customtkinter.CTkButton(master=self,text="Generate",command=lambda:generate(master.get()))
        self.generate_button.grid(row=3,column=2,sticky="es",padx=10,pady=10)





class App(customtkinter.CTk):#MAIN APP WINDOW
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.iconbitmap("icon.ico")
        self.minsize(1000,530)
        self.resizable(False,False)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.started=False
        self.save=open_save()

        self.grid_rowconfigure(0,weight=3)
        self.grid_rowconfigure(1,weight=1)

        self.title("AI Content Generation Tool")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0,1,2),weight=1)
        #self.grid_columnconfigure(1,weight=5)
        self.theme_frame=ThemeFrame(master=self)
        self.theme_frame.grid(padx=(20,10),pady=20,row=0,column=0,sticky="nsew")
        self.objects_frame=ObjectsFrame(master=self)
        self.objects_frame.grid(padx=10,pady=20,row=0,column=1,sticky="nsew")
        self.images_frame=ImagesFrame(master=self)
        self.images_frame.grid(padx=(10,20),pady=20,row=0,column=2,sticky="nsew")

        self.submit_frame=SubmitFrame(master=self)
        self.submit_frame.grid(padx=20,pady=(0,20),row=1,column=0,sticky="nsew",columnspan=3)

        #Progress Bar
        self.progress_bar=customtkinter.CTkProgressBar(master=self,height=20,corner_radius=0)
        self.progress_bar.grid(row=2,column=0,sticky="ew",columnspan=3)
        self.progress_bar.set(0)
        





    def get(self):
        try:
            if self.started:#Check that it's not already running
                printz("Already running!")
                return None

            #Object List
            object_list = self.objects_frame.object_list_entry.get('1.0', 'end-1c')
            object_list = re.split('[^a-zA-Z0-9 \'-]',object_list)
            for obj in object_list:
                if len(obj)<2:
                    object_list.remove(obj)

            #Word Count & Object word count - NUMBER LESS THAN 3000
            word_count = self.theme_frame.word_entry.get()
            object_word_count = self.objects_frame.word_entry.get()

            #Only check things needed
            theme=self.theme_frame.include_box.get()
            objects=self.objects_frame.include_box.get()
            images=self.images_frame.include_box.get()

            if len(self.submit_frame.key_entry.get())<10:
                printz("Must provide an openAI API KEY!")
                return None
            elif (not word_count.isdigit() or int(word_count)>3000) and theme==1:
                printz("Word count must not be empty and below 3000!")
                return None
            elif (len(object_list)>0 and (not object_word_count.isdigit() or int(object_word_count)>3000)) and objects==1:
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
                "theme?":theme,
                "objects?":objects,
                "images?":images
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
    while failed<3:
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

#Generate the article txt using chatGPT
def generate_article(theme,word_count,style,path):
    message = "Write a "+str(word_count)+" word text that will "+str(style)+" "+str(theme)
    text_body = ask_GPT(message)
    text_file = path+"/"+theme+".txt"
    with open(text_file,"w") as f:
        f.write(text_body)

#Generate each object txt using chatGPT
def generate_objects(object_list,word_count,style,path):#Gets multiple objects to process
    for obj in object_list:
        message = "Write a "+str(word_count)+" word text that will "+str(style)+" "+str(obj)
        text_body = ask_GPT(message)
        text_file = path+"/"+obj+".txt"
        with open(text_file,"w") as f:
            f.write(text_body)
    

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
                img.save(path+"/"+str(obj)+str(i)+".png","PNG")
            else:
                img.save(path+"/"+str(obj)+str(i)+".jpg")
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
        if not os.path.exists(path):
            os.mkdir(path)

        printz("Generation started...")
        app.started=True
        #1. Create new folder
        printz("1. Getting folder")
        
        app.progress_bar.set(0.1)
        #2. Generate article
        if data["theme?"]:
            printz("2. Generating article")
            generate_article(data["theme"],data["word_count"],data["theme_style"],path)
        else:
            printz("2. Skipped article")
        app.progress_bar.set(0.3)

        #3. Generate Objects
        if data["objects?"]:
            printz("3. Generating objects")
            generate_all_objects(data["object_list"],data["object_word_count"],data["objects_style"],path)
        else:
            printz("3. Skipped objects")
        app.progress_bar.set(0.6)

        #4. Generate Images
        if data["images?"]:
            if data["image_count"]!=0:
                printz("4. Generating Images")
                generate_all_images(data["object_list"],data["resolution"],data["image_count"],data["format"],data["images_style"],path)
        else:
            printz("4. Skipped images")

        printz("Completed!")
        app.progress_bar.set(1)
        app.started=False

    except:
        printz("ERROR: Generating the files")
        app.started=False
        app.progress_bar.set(0)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    if os.path.exists("theme.json"):
        customtkinter.set_default_color_theme("theme.json")
    app=App()
    app.mainloop()
