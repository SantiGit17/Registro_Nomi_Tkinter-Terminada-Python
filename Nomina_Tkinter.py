from tkinter import ttk
from tkinter import *

import sqlite3
from types import DynamicClassAttribute
from unittest import result
from winreg import QueryInfoKey

class Registro:
    db = 'Nomina_TkinterDavid'


    def __init__(self,window):
        self.wind = window
        self.wind.title('Nómina')

        #Create container
        frame = LabelFrame(self.wind, text = 'Register A New Person')
        frame.grid(row = 0, column=0, columnspan=3, pady=20)

        #N_Id
        Label(frame, 'Document Number: ').grid(row=1, column=0)
        self.document= Entry(frame)
        self.document.focus()
        self.document.grid(row=1,column= 1)

        #Name
        Label(frame, 'Name: ').grid(row=2, column=0)
        self.name= Entry(frame)
        self.name.grid(row=2,column= 1)

        #Last_Name
        Label(frame, 'Last Name: ').grid(row=3, column=0)
        self.Last_name= Entry(frame)
        self.Last_name.grid(row=3,column= 1)

        #Button save register
        ttk.Button(frame, text='Save register', command= self.add_product).grid(row=4, column=2, sticky=W+E)
        
        #Output Messages  
        self.message = Label(text= '', fg = 'red')
        self.message.grid(row= 4, column= 0, columnspan= 2, sticky= W + E)

        #Table
        self.tree = ttk.Treeview(height=10, columns=3)
        self.tree.grid(row=5, column=0, columnspan=1)
        self.tree.heading('#0', Text= 'Document Number', anchor=CENTER)
        self.tree.heading('#1', Text= 'Name', anchor=CENTER)
        self.tree.heading('#2', Text= 'Last Name', anchor=CENTER)
        #---
        self.tree.heading('#2', Text= 'Days worked', anchor=CENTER)
        self.tree.heading('#3', Text= 'Salary per month', anchor=CENTER)
        self.tree.heading('#4', Text= 'Base salary', anchor=CENTER)
        self.tree.heading('#5', Text= 'Subsidy of transport', anchor=CENTER)
        self.tree.heading('#6', Text= 'Salary and transport', anchor=CENTER)
        self.tree.heading('#7', Text= 'Discount', anchor=CENTER)
        self.tree.heading('#8', Text= 'Total Salary', anchor=CENTER)

        #Buttons
        ttk.Button(text= 'DELETE', command= self.delete_product).grid(row= 6, column= 0, sticky= W + E)
        ttk.Button(text= 'EDIT', command= self.edit_product).grid(row= 6, column= 1, sticky= W + E)


        #Llenado las filas(Filling the ROW)
        self.get_register

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.Nomina_TkinterDavid) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_register(self):
        records = self.tree.get_children()
        for element in records:
                self.run_query(query)
        #Consulta(quering) de datos        
        query ='SELECT * FROM Registro ORDER BY name DESC'
        db_rows= self.run_query(query)
        #Acomodar datos
        for row in db_rows:
            self.tree.insert('', 0, text= row[1], values= row[2])

    # User Input Validation
    def validation(self):
        return len(self.document.get()) != 0 and len(self.name.get()) != 0  and len(self.Last_name.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO Registro VALUES(NULL, ?, ?)'
            parameters =  (self.document.get(), self.name.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Register {} added Successfully'.format(self.name.get())
            self.document.delete(0, END)
            self.name.delete(0, END) 
            self.Last_name.delete(0,END)       
        else:
            self.message['text'] = 'Number Document, Name and Last Name is Required'
        self.get_register()
#----
    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Register'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Registro WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Register {} deleted Successfully'.format(name)
        self.get_register()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Register'
            return
        old_document = self.tree.item(self.tree.selection())['values'][0]
        name = self.tree.item(self.tree.selection())['text']
        old_Last_name = self.tree.item(self.tree.selection())['text']
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Register'
        
        # Old document 
        Label(self.edit_wind, text = 'Old document:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_document), state = 'readonly').grid(row = 1, column = 1)
        # New Name
        Label(self.edit_wind, text = 'New document:').grid(row = 2, column = 1)
        new_document= Entry(self.edit_wind)
        new_document.grid(row = 3, column = 1)

        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 5, column = 1)
        # New document
        Label(self.edit_wind, text = 'New name:').grid(row = 6, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 7, column = 1)

        #Old Last Name
        Label(self.edit_wind, text = 'Old Last Name:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_Last_name), state = 'readonly').grid(row = 9, column = 1)
        # New Last Name
        Label(self.edit_wind, text = 'New Last Name:').grid(row = 10, column = 1)
        new_Last_name = Entry(self.edit_wind)
        new_Last_name.grid(row = 11, column = 1)

        Button(self.edit_wind, text = 'Update', 
        command = lambda: self.edit_records(new_document.get(), old_document, new_name.get(), name, new_Last_name.get(), old_Last_name)).grid(row = 12, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_document, old_document, new_Last_name, old_Last_name):
        query = 'UPDATE Registro SET document = ?, name = ?, Last_name = ? WHERE document = ? AND name = ? AND Last_name = ?'
        parameters = (new_name, new_document, new_Last_name, name, old_document, old_Last_name)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Register {} updated successfylly'.format(name)
        self.get_register()
 
if __name__ == '__main__':
    window = Tk()
    application = Registro(window)
    window.mainloop() 

""" <<<Crear Base de dates (SQL Work...)>>>
    Create table Nomina_TkinterDavid(
    id INTEGER NOT NULL AUTOINCREMET,
    document FLOAT NOT NULL,
    name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    ---
    Daysworked INTEGER NOT NULL,
    Salary_month INTEGER NOT NULL,
    Base_salary FLOAT NOT NULL,
    Subsidy_Trans FLOAT NOT NULL,
    Salary_and_trans FLOAT NOT NULL,
    Descuento FLOAT NOT NULL,
    Total_Salary FLOAT NOT NULL);""" 