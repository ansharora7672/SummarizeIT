import tkinter as Tk
import customtkinter as CTk
from youtube import get_youtube_transcript
import chatgpt
import json
import tkinter.simpledialog as simpledialog
import os
from tkinter import messagebox
from chatgpt import chatgpt_api

class GUI():

    def __init__(self):
        # Set Application default theme to dark-mode with blue themed widgets
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("blue")
        self.recent_chats = {}  
        self.setup_ui()
        # self.load_chats_from_json()
        self.global_response = None
        self.folder_path = r"C:\Users\arora\Downloads\try"
# self.root.nav_bar_frame = CTk.CTkFrame(master=self.root, width=300, bg_color="#000000", fg_color="#000000", corner_radius=0)
     #       self.root.nav_bar_frame.pack(side="left", fill="y")


        self.process_and_create_buttons(self.folder_path)

        
    

    def setup_ui(self):
        self.root = CTk.CTk()
        self.root.title("SummarizeIT")
        self.root.geometry("1920x1080")

        self.root.title_frame = CTk.CTkFrame(master=self.root, corner_radius=0)
        self.root.title_frame.pack(side="top", fill="x")
        
        # Create a label within the frame for your application title
        self.root.title_label = CTk.CTkLabel(master=self.root.title_frame, text="SummarizeIT", font=("Roboto Medium", -16))
        self.root.title_label.pack(pady=10)
        
        
        self.root.nav_bar_frame = CTk.CTkFrame(master=self.root, width=300, bg_color="#000000", fg_color="#000000", corner_radius=0)
        self.root.nav_bar_frame.pack(side="left", fill="y")
        
        # Create a frame for the chat portion on the right
        self.root.chat_frame = CTk.CTkFrame(master=self.root, bg_color="#343541", fg_color="#343541", corner_radius=0)
        self.root.chat_frame.pack(side="right", fill="both", expand=True)

        # Create a label for "Recent Searches" title in the navigation bar
        self.root.recent_searches_label = CTk.CTkLabel(master=self.root.nav_bar_frame, text="Recent Searches", font=("Roboto Medium", -20))
        self.root.recent_searches_label.pack(side="top", fill="x", padx=30, pady=30)

        self.new_chat_button = CTk.CTkButton(master=self.root.chat_frame, text="New Chat", command=self.new_chat)
        self.new_chat_button.pack(side="top", padx=20, pady=5, anchor="e")


        # Create a text entry field for pasting the YouTube video URL
        self.root.url_entry = CTk.CTkEntry(master=self.root.chat_frame, placeholder_text="Paste YouTube Video URL here", width=900, height=40, corner_radius=10)
        self.root.url_entry.pack(side="top", padx=20, pady=30)

        
        
        # Create a text entry field for pasting the doubt entry.
        self.root.doubt_entry = CTk.CTkEntry(master=self.root.chat_frame,
                                            placeholder_text="Doubt Solver - Ask your Questions !! Start Typing ...",
                                            width=900,
                                            height=40,
                                            corner_radius=5)
        self.root.doubt_entry.pack(side="bottom", padx=20, pady=30)


# Bind the on_enter function to the Enter key for doubt_entry
        self.root.doubt_entry.bind("<Return>", self.on_enter)

        #self.root.url_entry.bind("<Return>", self.on_enter)


        # Create a frame for the response
        self.response_frame = CTk.CTkFrame(master=self.root.chat_frame, bg_color="#343541", fg_color="#343541", corner_radius=30)
        self.response_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        # Create the standard Text widget for displaying chat responses
        self.response_text = Tk.Text(self.response_frame, wrap="word", bg="#343541", fg="#FFFFFF", insertbackground="white", font = 14)
        
        # Create the Scrollbar for the Text widget
        self.response_scrollbar = Tk.Scrollbar(self.response_frame, command=self.response_text.yview)
        self.response_text['yscrollcommand'] = self.response_scrollbar.set

        # Pack the Scrollbar and then the Text widget into the frame
        self.response_scrollbar.pack(side="right", fill="y", expand=False)
        self.response_text.pack(side="left", fill="both", expand=True)



    def new_chat(self):
        chat_title = simpledialog.askstring("New Chat", "Enter the title of the new chat:")
        if chat_title:
            #self.create_chat_frame(chat_title)
            self.create_chat_button(chat_title)
            self.add_to_recent_chats(chat_title)
            self.save_chat_to_json(chat_title, self.global_response, self.root.url_entry.get())
            self.response_text.delete(1.0, Tk.END)
            self.root.url_entry.delete(0, Tk.END)
            self.root.doubt_entry.delete(0, Tk.END)

    # Add a method to create chat buttons dynamically in the navigation bar
    def create_chat_button(self, chat_title):
        title = chat_title
        chat_button = CTk.CTkButton(self.root.nav_bar_frame, text=chat_title, command=lambda: self.load_chat(title), height = 45, width = 270)
        chat_button.pack(side="top", padx=50, pady=7)


    def process_and_create_buttons(self, folder_path):
        # Iterating over each file in the specified folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)

                # Read the JSON file and extract the title
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    title = data.get("title", "Default Title")

                # Calling the create_chat_button function with the extracted title
                self.create_chat_button(title)


    def create_chat_frame(self, chat_title):
        # Ensure self.recent_chats is a dictionary
        chat_frame = CTk.CTkFrame(master=self.root.chat_frame, bg_color="#343541", fg_color="#343541", corner_radius=0)
        chat_frame.pack(side="top", fill="both", expand=True)
        chat_frame.pack_forget()  
        self.recent_chats[chat_title] = {
            "frame": chat_frame,
            "content": ""
        }


    def add_to_recent_chats(self, chat_title):
        # Assuming self.recent_chats is now a dictionary
        # if chat_title not in self.recent_chats:
        #     #self.create_chat_frame(chat_title)
        #     #self.create_chat_button(chat_title)
        pass


    # def load_chat(self, chat_title):
    #     # Hide all chat frames
    #     for chat in self.recent_chats.values():
    #         chat["frame"].pack_forget()

    #     # Load the content from the saved JSON
    #     try:
    #         with open(f'{chat_title}.json', 'r') as f:
    #             chat_data = json.load(f)
    #             # Assuming you have a Text widget or similar in each frame to display the content
    #             text_widget = Tk.Text(chat_frame, wrap="word", bg="#343541", fg="#FFFFFF", insertbackground="white")
    #             text_widget.pack(side="left", fill="both", expand=True)
    #             text_widget.delete(1.0, Tk.END)
    #             text_widget.insert(Tk.END, chat_data['content'])
    #             self.response_text.delete(1.0, Tk.END)
    #             self.response_text.insert(Tk.END, chat_data['content'])
    #     except FileNotFoundError:
    #         messagebox.showerror("Error", f"Chat '{chat_title}' not found.")


    def load_chat(self, chat_title):
        # # Hide all chat frames
        # for chat in self.recent_chats.values():
        #     chat["frame"].pack_forget()

        # Load the content from the saved JSON
        try:
            with open(f'{chat_title}.json', 'r') as f:
                chat_data = json.load(f)

                # Update response frame
                self.response_text.delete(1.0, Tk.END)
                self.response_text.insert(Tk.END, chat_data['response'])

                # Update URL entry
                self.root.url_entry.delete(0, Tk.END)
                self.root.url_entry.insert(0, chat_data['URL'])
        except FileNotFoundError:
            messagebox.showerror("Error", f"Chat '{chat_title}' not found.")

    # here i am making a function which would work on the enter and generate the output
    def on_enter(self, event):
        # ... [existing code to get subtitles and prompt] ...
        subtitles = get_youtube_transcript(self.root.url_entry.get())
        prompt = subtitles + '\n MY QUESTION FROM THE CONTENT / TRANSCRIPT OF THIS YOUTUBE VIDEO - ' + self.root.doubt_entry.get()
        response = chatgpt.chatgpt_api(prompt)
        self.display_response(response)
        #chat_title = self.root.url_entry.get()  # Modify as needed to generate a unique title
        self.global_response = response
        #self.save_chat_to_json(chat_title, response, self.root.url_entry.get)

        
    
    def display_response(self, response):
        self.response_text.delete(1.0, "end")
        self.response_text.insert("end", response)

    
    def save_chat_to_json(self, chat_title, chat_content, URL):
        
        #safe_chat_title = chat_title.replace("https://www.youtube.com/watch?v=", "").replace("/", "_").replace(":", "_")
        chat_data = {
            "title": chat_title,
            "response": chat_content,
            "URL": URL
        }
        with open(f'{chat_title}.json', 'w') as f:
            json.dump(chat_data, f, indent=4)

    # def load_chats_from_json(self):
    #     # This method should load chat titles and create buttons for them
    #     try:
    #         with open('chats.json', 'r') as file:
    #             chat_titles = json.load(file)
    #         for chat_title in chat_titles:
    #             self.create_chat_button(chat_title)
    #             self.recent_chats.append(chat_title)
    #     except FileNotFoundError:
    #         self.recent_chats = []

    


# Create and run the GUI
my_gui = GUI()
my_gui.root.mainloop()
