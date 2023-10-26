from tkinter import *
from tkinter import messagebox, filedialog # the * does not import another module of code
from random import choice, randint, shuffle
import json
import pandas
import pyperclip


PADX = 5
PADY = 5
FONT = ("Arial", 13)


# ---------------------------- Export Password File ------------------------------- #
def export(event=None):
    export = pandas.read_json("./data.json")
    # print(export)
    file_export = filedialog.asksaveasfile(defaultextension='*.csv',
                                           filetypes=[
                                            ("Comma-Separated Values .csv", "*.csv"),   
                                            ("JavaScript Object Notation .json","*.json"),
                                            ("Text File .txt",".txt")   
                                           ])
    # print(file_export)
    if file_export:
        file_path = file_export.name  # Get the full file path
        file_extension = file_path.split('.')[-1].lower()  # Get the file extension
        
        if file_extension == "json":
            # Export to JSON
            export.to_json(file_path, indent=4)
        elif file_extension == "csv":
            # transpose data for csv file
            export_csv = pandas.DataFrame(export)
            export_csv = export_csv.transpose()
            export_csv = export_csv.reset_index()
            export_csv.columns = ["Website", "Email/Username", "Password"]
            # print(export_csv)
        
            # Export to CSV
            export_csv.to_csv(file_path, index=False, lineterminator='\n')
        elif file_extension == "txt":
            export_txt = pandas.DataFrame(export)
            export_txt = export_txt.transpose()
            export_txt = export_txt.reset_index()
            export_txt.columns = ["Website", "Email", "Password"]
            # print(export_txt)
            text = ""
            for index, row in export_txt.iterrows():
                # print(index,row.Website, row.Email, row.Password)
                text += row.Website + "  |  " + row.Email + "  |  " + row.Password + "\n"
            # print(text)
            with open(file_path, "w") as text_file:
                text_file.write(text)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    # print(website_input.get(), email_input.get(), password_input.get())
    website_name = website_input.get()
    email_name = email_input.get()
    password_name = password_input.get()
    new_data = {
        website_name: {
            "email": email_name,
            "password": password_name
        }
    }
    
    if not website_name or not email_name or not password_name:
        messagebox.showinfo(title="Oops", message="Bitch please. Make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file) # Read old data Of type dictionary
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)    
        else:      
            data.update(new_data) # Update old data with new data
             
            with open("data.json", "w") as data_file:  
                json.dump(data, data_file, indent=4) # Write, Saving updated data
        finally:   
            website_input.delete(0, END)
            password_input.delete(0, END)
            
            
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_name = website_input.get()
    # print(f"Webiste: {type(website_name)}")
    
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file) # Read old data Of type dictionary
            # print(data)
        email_name = data[website_name]["email"]
        password_name = data[website_name]["password"]
        messagebox.showinfo(title=website_name, message=f"Email: {email_name}\nPassword: {password_name}")
    except FileNotFoundError:
        messagebox.showinfo(title="File Error", message="No Data exists")
    except KeyError:
        if website_name != "":
            messagebox.showinfo(title="Data Error", message=f"No details for {website_name} exist")
        else:
            messagebox.showinfo(title="Error", message="No Website was entered.\nTry again.")
    else:
        pyperclip.copy(password_name)


# ---------------------------- COLOR THEME (DARK MODE) ------------------------------- #
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    update_mode_text()
    update_colors()
    save_mode_state()
    
# Function to update the mode button text
def update_mode_text():
    if dark_mode:
        dark_mode_button.config(text="Light Mode")
        # Add your dark mode code here
    else:
        dark_mode_button.config(text="Dark Mode")
        # Add your light mode code here

# Function to save the mode state to a JSON file
def save_mode_state():
    with open("mode_state.json", "w") as f:
        json.dump({"dark_mode": dark_mode}, f)

# Function to load the mode state from a JSON file
def load_mode_state():
    try:
        with open("mode_state.json", "r") as f:
            data = json.load(f)
            return data.get("dark_mode", True)  # Default to light mode if the file is empty
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    
# Function to update colors based on the mode
def update_colors():
    BACKGROUND_LIGHT = "#CCCCCC"
    FOREGROUND_LIGHT = "#000000"
    BACKGROUND_DARK = "#555555"
    FOREGROUND_DARK = "#FFFFFF"
    if dark_mode:
        # Update Main Window
        window.config(bg=BACKGROUND_DARK)
        canvas.config(bg=BACKGROUND_DARK)
        # Update Labels
        website_label.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        email_label.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        password_label.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        # Update Entries
        website_input.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        email_input.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        password_input.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        # Update Buttons
        gen_pass_button.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        add_button.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        dark_mode_button.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        search_button.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)

    else:
        # Update Main Window
        window.config(bg=BACKGROUND_LIGHT)
        canvas.config(bg=BACKGROUND_LIGHT)
         # Update Labels
        website_label.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        email_label.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        password_label.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        # Update Entries
        website_input.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        email_input.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        password_input.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        # Update Buttons
        gen_pass_button.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        add_button.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
        dark_mode_button.config(bg=BACKGROUND_DARK, fg=FOREGROUND_DARK)
        search_button.config(bg=BACKGROUND_LIGHT, fg=FOREGROUND_LIGHT)
           

# ---------------------------- UI SETUP ------------------------------- #


dark_mode = load_mode_state()
# Create Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Key Bindings
window.bind('<Control-e>', export)


# Canvases
# Logo for MyPass app
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=1)


# Labels
# Website Label
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=2, sticky=E)
website_label.config(padx=PADX,pady=PADY)

# Email Label
email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(column=0, row=3, sticky=E)
email_label.config(padx=PADX,pady=PADY)

# Password Label
password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0, row=4, sticky=E)
password_label.config(padx=PADX,pady=PADY)


# Entries
# Website Entry
website_input = Entry(width=23, font=FONT)
website_input.grid(column=1, row=2)
website_input.focus()

# Email Entry
email_input = Entry(width=35, font=FONT)
email_input.grid(column=1, row=3, columnspan=2)
email_input.insert(0, "pwever1993@gmail.com")

# Password Entry
password_input = Entry(width=23, font=FONT)
password_input.grid(column=1, row=4)


# Buttons
# Generate Password Button
gen_pass_button = Button(text="Generate Password", width=14, bg="#0CC100", command=generate_password)
gen_pass_button.grid(column=2,row=4)

# Add Button
add_button = Button(text="Add", width=44, command=add)
add_button.grid(column=1, row=5, columnspan=2)

# Add Button
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=2)

# Light/Dark Mode Button
dark_mode_button = Button(text="Dark Mode", width=10, command=toggle_theme)
update_mode_text()
update_colors()
dark_mode_button.grid(column=2, row=0)



# Menu Bar
menubar = Menu(window)
# File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Export (Ctrl+e)", command=export)
# Setup Menu Bar
menubar.add_cascade(label="File", menu=file_menu)


# Keep Window open
window.config(menu=menubar)
window.mainloop()