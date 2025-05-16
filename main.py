from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
               'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7',
               '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website= website_entry.get().lower()
    email= email_entry.get().title()
    password= password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not email or not website or not password:
        messagebox.showinfo(title="Oops",
                            message="Please make sure you haven't left any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                       f" \n{email}\n{password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json","r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}

            except FileNotFoundError:
                with open("data.json","w") as file:
                    json.dump(new_data, file, indent=4)

            else:
                data.update(new_data)

                with open("data.json","w") as file:
                    json.dump(data, file, indent=4)

            finally:
                    website_entry.delete(0, END)
                    email_entry.delete(0, END)
                    password_entry.delete(0, END)

# ---------------------------- SEARCH LIST FOR EXISTING DETAILS ------------------------------- #
def search_list():
    website_to_search = website_entry.get().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
            messagebox.showinfo(title="Oops",
                                message="You haven't created any details yet")
    else:
        if website_to_search in data:
            email_print = data[website_to_search]["email"]
            password_print = data[website_to_search]["password"]

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)

            website_entry.insert(0, website_to_search)
            email_entry.insert(0, email_print)
            password_entry.insert(0, password_print)

            pyperclip.copy(password_print)
        else:
            messagebox.showinfo(title="Oops",
                                message="No existing data found for this website")
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)




# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


logo_image = PhotoImage(file="logo.png")

my_canvas = Canvas(width=200, height=200)
my_canvas.create_image(100, 100, image=logo_image)
my_canvas.grid(column=1,row=0)

website_label= Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry= Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_label= Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry= Entry(width=53)
email_entry.grid(column=1, row=2, columnspan=2)


password_label= Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry= Entry(width=33)
password_entry.grid(column=1, row=3)


generate_password_button= Button(text="Generate Password", width=15, command=password_generator)
generate_password_button.grid(column=2, row=3)


add_button= Button(text="Add", width=44, command= save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=search_list)
search_button.grid(column=2, row=1)

window.update_idletasks()
w = window.winfo_width()
h = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)
window.geometry(f'+{x}+{y}')




window.iconphoto(False, logo_image)
window.mainloop()