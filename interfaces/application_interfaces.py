import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
from database.database import Database
from tkinter import messagebox
from datetime import datetime


class App(object):

    def __init__(self, parent):
        self.root = parent
        self.root.title("Main frame")
        self.root.geometry('400x460+100+100')

        btn_add_event = tk.Button(self.root, text="Agregar Evento", command=self.add_event_window)
        btn_add_event.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)

        btn_register = tk.Button(self.root, text="Registrar Reserva", command=self.register)
        btn_register.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)

        btn_list_event = tk.Button(self.root, text="Listado de  Eventos", command=self.list_events)
        btn_list_event.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)


    def hide(self):
        self.root.withdraw()

    def on_close(self, other_frame):
        other_frame.destroy()
        self.show()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def validation_of_integer_positive(self, entry):
        if len(entry) == 0:
            return True
        elif entry.isdigit() and int(entry) > 0:
            return True
        else:
            return False

    def validation_of_integer(self, entry):
        if len(entry) == 0:
            return True
        elif entry.isdigit():
            return True
        else:
            return False

    def validation_of_letters(self, entry):
        if len(entry) == 0:
            return True
        elif entry.isalpha():
            return True
        else:
            return False

    def add_event(self, name, number_chairs, date):
        if len(name) != 0 and len(number_chairs) != 0:
            database = Database()
            query = 'INSERT INTO Evento VALUES(NULL,?,?,?,?)'
            params = (str(name), str(date), int(number_chairs), 0)
            database.execute_query(query, params)
            messagebox.showinfo("Success", "El evento se guardo correctamente")
        else:
            messagebox.showerror("Error", "Algunos campos están vacíos")

    def add_event_window(self):
        self.hide()
        other_frame = tk.Toplevel()
        other_frame.geometry("400x300")
        other_frame.title("Agregar evento")

        tk.Label(other_frame, text='Nombre:', font=("Futura Md BT", 12)).grid(row=0, column=0, pady=10)
        entry_name = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_name, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_letters), '%P')).grid(row=0,
                                                                                                column=1,
                                                                                                pady=10)

        tk.Label(other_frame, text='Fecha:', font=("Futura Md BT", 12)).grid(row=1, column=0)
        date = DateEntry(other_frame, width=17, background='darkblue', foreground='white', borderwidth=2,
                         date_pattern='yyyy-mm-dd')
        date.grid(row=1, column=1, pady=10)

        tk.Label(other_frame, text='Numero de asistentos:', font=("Futura Md BT", 12)).grid(row=2, column=0, pady=10)
        entry_chairs_var = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_chairs_var, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_integer_positive), '%P')).grid(row=2,
                                                                                                         column=1,
                                                                                                         pady=10)
        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=4, column=0, pady=20)

        validate = lambda: self.add_event(entry_name.get(), entry_chairs_var.get(), date.get())
        btn_save = tk.Button(other_frame, text="Guardar", command=validate, width=20)
        btn_save.grid(row=4, column=1, pady=20)

    def register(self):
        self.hide()
        other_frame = tk.Toplevel()
        other_frame.geometry("400x500")
        other_frame.title("registrar reserva")

        tk.Label(other_frame, text='Correo:', font=("Futura Md BT", 12)).grid(row=1, column=0, pady=10)
        entry_email = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_email, width=20).grid(row=1, column=1, pady=10)

        tk.Label(other_frame, text='Nombre:', font=("Futura Md BT", 12)).grid(row=2, column=0, pady=10)
        entry_name = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_name, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_letters), '%P')).grid(row=2, column=1,
                                                                                                pady=10)

        tk.Label(other_frame, text='Apellido paterno:', font=("Futura Md BT", 12)).grid(row=3, column=0, pady=10)
        entry_apellido_paterno = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_apellido_paterno, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_letters), '%P')).grid(row=3, column=1,
                                                                                                pady=10)

        tk.Label(other_frame, text='Apellido Materno:', font=("Futura Md BT", 12)).grid(row=4, column=0, pady=10)
        entry_apellido_materno = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_apellido_materno, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_letters), '%P')).grid(row=4, column=1,
                                                                                                pady=10)

        tk.Label(other_frame, text='Telefono:', font=("Futura Md BT", 12)).grid(row=5, column=0, pady=10)
        entry_tlf = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_tlf, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_integer), '%P')).grid(row=5, column=1,
                                                                                                pady=10)

        tk.Label(other_frame, text='Empresa:', font=("Futura Md BT", 12)).grid(row=6, column=0, pady=10)
        entry_company = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_company, width=20).grid(row=6, column=1, pady=10)

        tk.Label(other_frame, text='Puesto:', font=("Futura Md BT", 12)).grid(row=7, column=0, pady=10)
        entry_job_post = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_job_post, width=20, validate="key",
                 validatecommand=(other_frame.register(self.validation_of_letters), '%P')).grid(row=7, column=1,
                                                                                                pady=10)

        list_id, list_name = self.list_combobox()
        tk.Label(other_frame, text='Evento:', font=("Futura Md BT", 12)).grid(row=8, column=0, pady=10)
        combobox = ttk.Combobox(other_frame, width=20, values=list_name)
        combobox.grid(row=8, column=1, pady=10)
        combobox.current(0)

        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=9, column=0, pady=20, padx=5)

        save_register = lambda: self.seve_register(entry_email.get(), entry_name.get(), entry_apellido_paterno.get(),
                                                   entry_apellido_materno.get(), entry_tlf.get(), entry_company.get(),
                                                   entry_job_post.get(), list_id[combobox.current()])
        btn_save = tk.Button(other_frame, text="Guardar", command=save_register, width=20)
        btn_save.grid(row=9, column=1, pady=20, padx=5)

    def list_combobox(self):
        database = Database()
        dataset = database.get_list_events()
        list_id = []
        list_name = []
        date_now = datetime.now().date()
        for data in dataset:
            if data[2] >= str(date_now):
                list_id.append(data[0])
                list_name.append(data[1])
        return list_id, list_name

    def seve_register(self, correo, nombre, apellido_paterno, apellido_materno,
                      telefono, nombre_empresa, puesto, evento_id):
        validation = len(correo) != 0 and len(nombre) != 0 and len(apellido_materno) != 0 and \
                     len(apellido_paterno) != 0 and len(telefono) != 0 and len(nombre_empresa) != 0 and len(puesto) != 0
        if validation:

            query_evento = 'SELECT * FROM Evento WHERE id={}'.format(int(evento_id))
            database = Database()
            data = database.execute_query(query_evento)
            value_reserva = None
            value_total = None
            for row in data:
                value_reserva = row[4]
                value_total = row[3]
            if value_total == value_reserva:
                messagebox.showerror("Error", "Los puestos del evento estan agotados")
            else:
                query_asistente = 'INSERT INTO Asistente VALUES(?,?,?,?,?,?,?)'
                query_comprobante = 'INSERT INTO Comprobante VALUES(NULL,?,?,?,?)'
                query_evento = 'UPDATE Evento SET numero_asientos_reservados = {} where id = {}'.format(
                    value_reserva + 1,
                    int(evento_id))
                params_asistente = (
                str(correo), str(nombre), str(telefono), str(apellido_materno), str(apellido_paterno),
                str(nombre_empresa), str(puesto))
                params_comprobante = (str(datetime.now().date()), "pendiente por pagar", str(correo), int(evento_id))
                database.execute_query(query_asistente, params_asistente)
                database.execute_query(query_comprobante, params_comprobante)
                database.execute_query(query_evento)
                messagebox.showinfo("Success", "Los datos fueron guardados correctamente")
        else:
            messagebox.showerror("Error", "Algunos campos están vacíos")

    def list_events(self):
        self.hide()
        database = Database()
        dataset = database.get_list_events()
        other_frame = tk.Toplevel()
        other_frame.geometry("1050x400")
        other_frame.title("Listado de eventos")

        table = ttk.Treeview(other_frame, columns=("nombre", "fecha", "numero_asientos", "numeros_asistos_reservados"))
        table.grid(row=1, column=0, columnspan=5, pady=20, padx=10)
        table.heading("#0", text="id")
        table.heading("nombre", text="nombre")
        table.heading("fecha", text="fecha")
        table.heading("numero_asientos", text="numeros de asientos")
        table.heading("numeros_asistos_reservados", text="numero de asientos reservados")
        for data in dataset:
            table.insert("", tk.END, text=str(data[0]), values=(str(data[1]),
                                                                str(data[2]),
                                                                str(data[3]),
                                                                str(data[4])))

        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=2, column=0, padx=20, pady=20, columnspan=3)

        btn_save = tk.Button(other_frame, text="Detalle", command=handler, width=20)
        btn_save.grid(row=2, column=2, pady=20, columnspan=2)


