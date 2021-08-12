from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                    [random.choice(numbers) for _ in range(nr_numbers)] + \
                    [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    password = "".join(password_list)

    pass_entry.delete(0, END)
    pass_entry.insert(0, f"{password}")

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = pass_entry.get()
    new_data = {website: {
        "username": username,
        "password": password,
    }}
    # Check for empty entries
    if not all((website, username, password)):
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Check if website exist in data file
            if website in data:
                # Ask the user if data should be updated
                if messagebox.askyesno(title=f"Credential for {website}",
                                           message=f"Credentials for {website}"
                                                   f" exist in data file.\n Update?"):
                    data.update(new_data)
                    # Write new data
                    with open("data.json", mode="w") as data_file:
                        json.dump(data, data_file, indent=4)
            else:
                data.update(new_data)
                # Write new data
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
        finally:
            clear_entries()


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    if website:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showwarning(title="Warning", message="Data File not Found")
        else:
            if website in data:
                pass_entry.delete(0, END)
                username_entry.delete(0, END)
                username_entry.insert(0, f"{data[website]['username']}")
                pass_entry.insert(0, f"{data[website]['password']}")
                # messagebox.showinfo(title=f"credentials for {website}",
                #                     message=f"username: {data[website]['username']}\n"
                #                             f"password: {data[website]['password']}")
            else:
                messagebox.showwarning(title="Warning", message=f"Credentials for {website} not found")


def clear_entries():
    website_entry.delete(0, END)
    pass_entry.delete(0, END)
    username_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

logo_img = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, sticky="we")

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky='e')

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2, sticky='e')

pass_label = Label(text="Password:")
pass_label.grid(column=0, row=3, sticky='e')

# Entries

website_entry = Entry()
website_entry.grid(column=1, row=1, sticky='we')
website_entry.focus()

username_entry = Entry()
username_entry.grid(column=1, row=2, columnspan=2, sticky='we')
# username_entry.insert(0, "name@example.com")

pass_entry = Entry()
pass_entry.grid(column=1, row=3, sticky='we')

# Buttons

generate_pass_btn = Button(text="Generate Password", command=generate_password)
generate_pass_btn.grid(column=2, row=3, sticky='we')

add_btn = Button(text="Add", width=36, command=save)
add_btn.grid(column=1, row=4, columnspan=2, sticky='we')

search_btn = Button(text="Search", command=find_password)
search_btn.grid(column=2, row=1, sticky='we')

window.mainloop()
