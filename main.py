import customtkinter
import sqlite3
import uuid
from tkinter import messagebox

connection = sqlite3.connect("BancoDeDados.db")
cursor = connection.cursor()

try:
    cursor.execute("SELECT * FROM contacts ORDER BY name")
except sqlite3.OperationalError as error:
    print(error)
    sql_command = """CREATE TABLE contacts (
        name VARCHAR(30),
        description VARCHAR(30),
        id VARCHAR(32) )"""
    cursor.execute(sql_command)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x550")
root.title("Vidraçaria Popular")

Name = customtkinter.StringVar()
Description = customtkinter.StringVar()
Id = customtkinter.StringVar()

def AddContact():
    if Name.get() != "" and Description.get() != "":   
        cursor.execute("INSERT INTO contacts VALUES (?, ?, ?)", (Name.get(), Description.get(), uuid.uuid4().hex))
        connection.commit()

        SetList()
        EntryReset()
        messagebox.showinfo("Confirmação", "Sucesso ao adcionar cliente!")

    else:
        messagebox.showerror("Erro","Favor, preencha informações")

def UpdateContact():
    if Name.get() != "" and Description.get() != "":
        cursor.execute(f"UPDATE contacts SET name = '{Name.get()}' WHERE id = '{Id.get()}'")
        cursor.execute(f"UPDATE contacts SET description = '{Description.get()}' WHERE id = '{Id.get()}'")
        connection.commit()
        messagebox.showinfo("Confirmação", "Sucesso ao atualizar Cliente")
        EntryReset()
        SetList()
    else:
        messagebox.showerror("Erro", "Favor, preencha informações")

def DeleteContact():
    if Name.get() != "" and Description.get() != "" and Id.get != "":
        result = messagebox.askyesno('Confirmação','Quer mesmo apagar?')
        if result == True:
            cursor.execute(f"DELETE FROM contacts WHERE id = '{Id.get()}'")
            connection.commit()
            SetList()
    else:
        messagebox.showerror("Erro", "Favor, selecionar o Nome")

def EntryReset():
    Name.set("")
    Description.set("")
    Id.set("")

def Exit():
    connection.close()
    root.destroy()

def ButtonClicked(id:str):
    cursor.execute(f"SELECT name, description FROM contacts WHERE id = '{id}'")
    list_contacts = cursor.fetchall()

    Name.set(list_contacts[0][0])
    Description.set(list_contacts[0][1])
    Id.set(id)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="A Vidraçaria Popular", font=("Times new roman",50))
label.pack(pady=12, padx=10)

entryName = customtkinter.CTkEntry(master=frame, textvariable=Name, font=("Times new roman",20), width=500).place(x=30, y=100)
entryDescription = customtkinter.CTkEntry(master=frame, textvariable=Description, font=("Times new roman",20), width=500).place(x=30, y=150)

buttonAdd = customtkinter.CTkButton(master=frame, text="Adicionar", command=AddContact, font=("Times new roman",20)).place(x=30, y=200)
buttonUpdate = customtkinter.CTkButton(master=frame, text="Atualizar", command=UpdateContact, font=("Times new roman",20)).place(x=30, y=250)
buttonDelete = customtkinter.CTkButton(master=frame, text="Apagar", command=DeleteContact, font=("Times new roman",20)).place(x=180, y=250)
buttonReset = customtkinter.CTkButton(master=frame, text="Resetar", command=EntryReset, font=("Times new roman",20)).place(x=180, y=200)
buttonExit = customtkinter.CTkButton(master=frame, text="Sair", command=Exit, font=("Times new roman",20)).place(x=30, y=450)

def SetList():
    cursor.execute("SELECT * FROM contacts ORDER BY name")
    list_contact = cursor.fetchall()
    frameSelect = customtkinter.CTkScrollableFrame(master=frame, height=350, width=250, label_text="List")
    frameSelect.place(x=600, y=100)
    for i, list in enumerate(list_contact):
        new_button = customtkinter.CTkButton(master=frameSelect, text=f"{i + 1}: {list[0]}", command=ButtonClicked)
        new_button = customtkinter.CTkButton(master=frameSelect, text=list[0], command=lambda id=list[2]: ButtonClicked(id))
        new_button.pack(pady=10)
    
SetList()
root.mainloop()
connection.close()
