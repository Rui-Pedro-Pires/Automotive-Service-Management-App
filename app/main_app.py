from tkinter import Tk, Button, Label, Event, LabelFrame, LEFT, Toplevel, Frame, IntVar, Checkbutton, Menubutton, Scrollbar, Listbox, StringVar, Entry, Menu, W, E, N, S, RAISED, GROOVE, FLAT, PhotoImage,END
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from horario_list import horario_list
import mysql.connector

def delete():
    clientId = s1.get()
    serviço = s2.get()
    args = (clientId, serviço)
    if messagebox.askyesno("Eliminiar", "Tem a certeza que pretende eliminar o resgisto selecionado?"):
        query = "DELETE FROM cliente_serviços WHERE clienteID = %s AND serviço = %s LIMIT 1"
        conn = mysql.connector.connect(
                host="sql8.freesqldatabase.com",
                user="sql8704076",
                password="DWIEWlMnpi",
                database="sql8704076"
                )
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        cursor.close()
        conn.close()
        clear(trv)
    else:
        return True

def on_closing(app, root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()
        root.deiconify()

def grep_data(event):
    row_id = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    s1.set(item['values'][0])
    data_marcação_text.set(item['values'][1])
    hora_marcação_entry.set(item['values'][2])
    data_entrega_text.set(item['values'][3])
    hora_entrega_entry.set(item['values'][4])
    cliente_entry.set(item['values'][5])
    marca_entry.set(item['values'][6])
    modelo_entry.set(item['values'][7])
    matricula_entry.set(item['values'][8])
    s2.set(item['values'][9])
    service_box.selection_clear(0, END)
    index = service_box.get(0, "end").index(s2.get())
    service_box.select_set(index)

def submit(trv, service_box):
    selected_index = service_box.curselection()
    selected_services = []
    for index in selected_index:
        selected_services.append(service_box.get(index))
    conn = mysql.connector.connect(
            host="sql8.freesqldatabase.com",
            user="sql8704076",
            password="DWIEWlMnpi",
            database="sql8704076"
            )
    cursor = conn.cursor()

    query = "INSERT INTO clientes (data_marcação, hora_marcação, data_entrega, hora_entrega, cliente, telemovel, email, matricula, marca, modelo, kmx, ano) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (
        data_marcação_text.get(),
        hora_marcação_entry.get(),
        data_entrega_text.get(),
        hora_entrega_entry.get(),
        cliente_entry.get(),
        telem_entry.get(),
        email_entry.get(),
        matricula_entry.get(),
        marca_entry.get(),
        modelo_entry.get(),
        str(kms_entry.get()),
        str(ano_entry.get())
    )

    cursor.execute(query, vals)
    conn.commit()
    query_search_id = "SELECT id FROM clientes WHERE cliente = '" + cliente_entry.get() + '\''
    cursor.execute(query_search_id)
    clienteID = cursor.fetchall()
    clienteID = int(str(clienteID[0]).strip('(),'))
    for service in selected_services:
        cursor.execute("INSERT INTO cliente_serviços VALUES (%s, %s)", (clienteID, str(service)))
    conn.commit()
    cursor.close()
    conn.close()
    
    hora_marcação_entry.delete(0, 'end')
    hora_entrega_entry.delete(0, 'end')
    cliente_entry.delete(0, 'end')
    telem_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    matricula_entry.delete(0, 'end')
    marca_entry.delete(0, 'end')
    modelo_entry.delete(0, 'end')
    kms_entry.delete(0, 'end')
    ano_entry.delete(0, 'end')
    service_box.selection_clear(0, END)
    
    clear(trv)


def clear(trv):
    conn = mysql.connector.connect(
  host="sql8.freesqldatabase.com",
  user="sql8704076",
  password="DWIEWlMnpi",
  database="sql8704076"
)
    cursor = conn.cursor()
    cursor.execute("SELECT data_marcação, hora_marcação, data_entrega, hora_entrega, cliente, marca, modelo, matricula, cliente_serviços.serviço FROM clientes JOIN cliente_serviços ON id = clienteID")
    clientes = cursor.fetchall()
    insert(clientes, trv)
    cursor.close()
    conn.close()

def insert(clientes, trv):
    trv.delete(*trv.get_children())
    for cliente in clientes:
        trv.insert('', 'end', values=cliente)
    
def search(str, trv):
    str1 = str.get()
    conn = mysql.connector.connect(
  host="sql8.freesqldatabase.com",
  user="sql8704076",
  password="DWIEWlMnpi",
  database="sql8704076"
)
    cursor = conn.cursor()
    query = "SELECT clientes.data_marcação, clientes.hora_marcação, clientes.data_entrega, clientes.hora_entrega, clientes.cliente, clientes.marca, clientes.modelo, clientes.matricula, cliente_serviços.serviço FROM clientes JOIN cliente_serviços ON clientes.id = cliente_serviços.clienteID WHERE clientes.cliente LIKE '%"+str1+"%'"
    cursor.execute(query)
    clientes = cursor.fetchall()
    insert(clientes, trv)
    cursor.close()
    conn.close()

def limpar():
    hora_marcação_entry.delete(0, 'end')
    hora_entrega_entry.delete(0, 'end')
    cliente_entry.delete(0, 'end')
    telem_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    matricula_entry.delete(0, 'end')
    marca_entry.delete(0, 'end')
    modelo_entry.delete(0, 'end')
    kms_entry.delete(0, 'end')
    ano_entry.delete(0, 'end')
    service_box.selection_clear(0, END)

def    main_app(root):
    app = Toplevel(root)
    root.withdraw()
    app.title("Serviços")
    app.config(background="white")
    app.geometry("1920x1080")
    app.resizable(False, False)
    

#######################     COSTUMER SECTION        ####################################
    
    costumer_label = LabelFrame(app, text="Lista de Clientes")
    search_label = LabelFrame(app, text="Consultar")
    data_label = LabelFrame(app, text="Informações")
    serviço_label = LabelFrame(data_label, text="Serviços")

    costumer_label.pack(fill="both", expand="yes", padx=20, pady=10)
    search_label.pack(fill="both", expand="yes", padx=20, pady=10)
    data_label.pack(fill="both", expand="yes", padx=20, pady=10)
    serviço_label.place(x=1100, y=0)

    global s1
    global s2
    s1 = StringVar()
    s2 = StringVar()

    global trv
    trv = ttk.Treeview(costumer_label, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=15)
    trv.pack(fill="both")

    trv.heading(1, text="Data de marcação")
    trv.heading(2, text="Hora de marcação")
    trv.heading(3, text="Data de entrega")
    trv.heading(4, text="Hora de entrega")
    trv.heading(5, text="Cliente")
    trv.heading(6, text="Marca")
    trv.heading(7, text="Modelo")
    trv.heading(8, text="Matricula")
    trv.heading(9, text="Serviços")

    trv.bind('<Double 1>', grep_data)
    
    conn = mysql.connector.connect(
            host="sql8.freesqldatabase.com",
            user="sql8704076",
            password="DWIEWlMnpi",
            database="sql8704076"
            )
    cursor = conn.cursor()
    cursor.execute("SELECT data_marcação, hora_marcação, data_entrega, hora_entrega, cliente, marca, modelo, matricula, cliente_serviços.serviço FROM clientes JOIN cliente_serviços ON id = clienteID")
    clientes = cursor.fetchall()
    insert(clientes, trv)

###########################      SEARCH    ###########################    
    
    str = StringVar()
    search_lbl = Label(search_label, text="Consultar")
    search_lbl.pack(side=LEFT, padx=10)
    ent = Entry(search_label, textvariable=str)
    ent.pack(side=LEFT, padx=6)
    Button(search_label, text="Search", command=lambda: search(str, trv)).pack(side=LEFT, padx=6)
    Button(search_label, text="Clear", command=lambda: clear(trv)).pack(side=LEFT, padx=6)

###########################     DATA SECTION        #################################

    cursor.execute("SELECT DISTINCT cliente FROM clientes")
    cliente_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT matricula FROM clientes")
    matricula_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT marca FROM clientes")
    marca_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT modelo FROM clientes")
    modelo_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT serviço FROM serviços")
    serviços = cursor.fetchall()

    global data_marcação_text
    data_marcação_label = Label(data_label, text="Data de marcação").grid(row=0, column=0, padx=5, pady=3)
    data_marcação_text = StringVar()
    data_marcação_cal = DateEntry(data_label, textvariable=data_marcação_text, width=26, year=2024, month=5, day=22, background='57a1f8', foreground='white', borderwidth=1, date_pattern='MM/dd/yyyy')
    data_marcação_cal.grid(row=0, column=1, padx=5, pady=3)

    global hora_marcação_entry
    hora_marcação_label = Label(data_label, text="Hora de marcação").grid(row=1, column=0, padx=5, pady=3)
    hora_marcação_entry = ttk.Combobox(data_label, values=horario_list, width=26)
    hora_marcação_entry.grid(row=1, column=1, padx=5, pady=3)

    global  data_entrega_text
    data_entrega_label = Label(data_label, text="Data de entrega").grid(row=2, column=0, padx=5, pady=3)
    data_entrega_text = StringVar()
    data_entrega_cal = DateEntry(data_label, textvariable=data_entrega_text, width=26, year=2024, month=5, day=22, background='57a1f8', foreground='white', borderwidth=1, date_pattern='MM/dd/yyyy')
    data_entrega_cal.grid(row=2, column=1, padx=5, pady=3)

    global hora_entrega_entry
    hora_entrega_label = Label(data_label, text="Hora de entrega").grid(row=3, column=0, padx=5, pady=3)
    hora_entrega_entry = ttk.Combobox(data_label, values=horario_list, width=26)
    hora_entrega_entry.grid(row=3, column=1, padx=5, pady=3)

    global cliente_entry
    cliente_label = Label(data_label, text="Cliente").grid(row=0, column=2, padx=5, pady=3)
    cliente_entry = ttk.Combobox(data_label, values=cliente_list, width=26)
    cliente_entry.grid(row=0, column=3, padx=5, pady=3)

    global matricula_entry
    matricula_label = Label(data_label, text="Matrícula").grid(row=1, column=2, padx=5, pady=3)
    matricula_entry = ttk.Combobox(data_label, values=matricula_list, width=26)
    matricula_entry.grid(row=1, column=3, padx=5, pady=3)

    global marca_entry
    marca_label = Label(data_label, text="Marca").grid(row=2, column=2, padx=5, pady=3)
    marca_entry = ttk.Combobox(data_label, values=marca_list, width=26)
    marca_entry.grid(row=2, column=3, padx=5, pady=3)

    global modelo_entry
    modelo_label = Label(data_label, text="Modelo").grid(row=3, column=2, padx=5, pady=3)
    modelo_entry = ttk.Combobox(data_label, values=modelo_list, width=26)
    modelo_entry.grid(row=3, column=3, padx=5, pady=3)

    global telem_entry
    telem_label = Label(data_label, text="Telemóvel").grid(row=0, column=4, padx=5, pady=3)
    telem_entry = Entry(data_label, width=26)
    telem_entry.grid(row=0, column=5, padx=5, pady=3)

    global email_entry
    email_label = Label(data_label, text="Email").grid(row=1, column=4, padx=5, pady=3)
    email_entry = Entry(data_label, width=26)
    email_entry.grid(row=1, column=5, padx=5, pady=3)

    global kms_entry
    kms_label = Label(data_label, text="Kilometers").grid(row=2, column=4, padx=5, pady=3)
    kms_entry = Entry(data_label, width=26)
    kms_entry.grid(row=2, column=5, padx=5, pady=3)

    global ano_entry
    ano_label = Label(data_label, text="Ano").grid(row=3, column=4, padx=5, pady=3)
    ano_entry = Entry(data_label, width=26)
    ano_entry.grid(row=3, column=5, padx=5, pady=3)

    global service_box
    service_box = Listbox(serviço_label, width=50, selectmode="multiple", relief=GROOVE)
    service_box.pack()
    tipo_servico = []
    for service_tuple in serviços:
        service_str = service_tuple[0]
        service_str = service_str.strip('(),\'\'')
        tipo_servico.append(service_str)

    for service in tipo_servico:
        service_box.insert('end', service)

            
    Button(data_label, text="Adicionar", command=lambda: submit(trv, service_box)).grid(row=4, column=0, padx=5, pady=3)
    Button(data_label, text="Atualizar", command="").grid(row=4, column=1, padx=5, pady=3)
    Button(data_label, text="Eliminar", command=delete).grid(row=4, column=2, padx=5, pady=3)
    Button(data_label, text="Limpar", command=limpar).grid(row=4, column=3, padx=5, pady=3)

    cursor.close()
    conn.close()

###############             Closing handle          #########################

    #Run the aplication
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app, root))
    app.mainloop()