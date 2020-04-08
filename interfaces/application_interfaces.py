import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk


class App(object):

    def __init__(self, parent):
        self.root = parent
        self.root.title("Main frame")
        self.root.geometry('400x460+100+100')

        btn_add_event = tk.Button(self.root, text="Agregar Evento", command=self.add_event)
        btn_add_event.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)

        btn_register = tk.Button(self.root, text="Registrar Reserva", command=self.register)
        btn_register.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)

        btn_list_event = tk.Button(self.root, text="Listado de  Eventos", command=self.list_event)
        btn_list_event.pack(fill=tk.X, padx=5, pady=5, ipadx=2, ipady=5)

    def hide(self):
        self.root.withdraw()

    def on_close(self, other_frame):
        other_frame.destroy()
        self.show()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def add_event(self):
        self.hide()
        other_frame = tk.Toplevel()
        other_frame.geometry("400x300")
        other_frame.title("Agregar evento")

        tk.Label(other_frame, text='Nombre:', font=("Futura Md BT", 12)).grid(row=0, column=0, pady=10)
        entry_name = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_name, width=20).grid(row=0, column=1, pady=10)

        tk.Label(other_frame, text='Fecha:', font=("Futura Md BT", 12)).grid(row=1, column=0)
        date = DateEntry(other_frame, width=17, background='darkblue', foreground='white', borderwidth=2)
        date.grid(row=1, column=1, pady=10)

        tk.Label(other_frame, text='Numero de asistentos:', font=("Futura Md BT", 12)).grid(row=2, column=0, pady=10)
        entry_chairs = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_chairs, width=20).grid(row=2, column=1, pady=10)

        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=4, column=0, pady=20)

        btn_save = tk.Button(other_frame, text="Guardar", command=handler, width=20)
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
        tk.Entry(other_frame, textvariable=entry_name, width=20).grid(row=2, column=1, pady=10)

        tk.Label(other_frame, text='Apellido paterno:', font=("Futura Md BT", 12)).grid(row=3, column=0, pady=10)
        entry_apellido_paterno = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_apellido_paterno, width=20).grid(row=3, column=1, pady=10)

        tk.Label(other_frame, text='Apellido Materno:', font=("Futura Md BT", 12)).grid(row=4, column=0, pady=10)
        entry_apellido_materno = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_apellido_materno, width=20).grid(row=4, column=1, pady=10)

        tk.Label(other_frame, text='Telefono:', font=("Futura Md BT", 12)).grid(row=5, column=0, pady=10)
        entry_tlf = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_tlf, width=20).grid(row=5, column=1, pady=10)

        tk.Label(other_frame, text='Empresa:', font=("Futura Md BT", 12)).grid(row=6, column=0, pady=10)
        entry_company = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_company, width=20).grid(row=6, column=1, pady=10)

        tk.Label(other_frame, text='Puesto:', font=("Futura Md BT", 12)).grid(row=7, column=0, pady=10)
        entry_job_post = tk.StringVar()
        tk.Entry(other_frame, textvariable=entry_job_post, width=20).grid(row=7, column=1, pady=10)

        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=8, column=0, pady=20, padx=5)

        btn_save = tk.Button(other_frame, text="Guardar", command=handler, width=20)
        btn_save.grid(row=8, column=1, pady=20, padx=5)

    def list_event(self):
        self.hide()
        other_frame = tk.Toplevel()
        other_frame.geometry("1050x400")
        other_frame.title("Listado de eventos")

        table = ttk.Treeview(other_frame, columns=("nombre", "fecha","numero_asientos","numeros_asistos_reservados"))
        table.grid(row=1, column=0, columnspan=5, pady=20,padx=10)
        table.heading("#0", text="codigo")
        table.heading("nombre", text="nombre")
        table.heading("fecha", text="fecha")
        table.heading("numero_asientos", text="numeros de asientos")
        table.heading("numeros_asistos_reservados", text="numero de asientos reservados")
        # table.grid(row=1, column=0, columnspan=3)

        handler = lambda: self.on_close(other_frame)
        btn = tk.Button(other_frame, text="Cancelar", command=handler, width=20)
        btn.grid(row=2, column=0, padx=20, pady=20, columnspan=3)

        btn_save = tk.Button(other_frame, text="Guardar", command=handler, width=20)
        btn_save.grid(row=2, column=2, pady=20, columnspan=2)
