import socket
import threading
import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox as messagebox
from tkinter import filedialog
import os
import sys



window = tk.Tk()
window.title("File transformer 3000")
window.geometry("300x200")

ip = ""
port = ""
port_entry = None
sc= False
cts = False

def create_server():
    global ip, port_entry
    
    for widget in button_frame.winfo_children():
        widget.pack_forget()
    try:
        hostname = socket.gethostname()
        def get_local_ip():
            try:
                # Vytvoření dočasného socketu pro získání lokální IP adresy
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                temp_socket.connect(("8.8.8.8", 80))  # Tato adresa může být libovolná
                local_ip = temp_socket.getsockname()[0]
                temp_socket.close()
                return local_ip
            except Exception as e:
                print(f"Nepodařilo se získat lokální IP adresu: {str(e)}")
                return None
        ip = get_local_ip()
        
    except socket.error as e:
        messagebox.showerror("Chyba", f"Nepodařilo se získat IP adresu: {str(e)}") 
        
    iplabel = tk.Label(button_frame, text=f"Ip: {ip}")
    iplabel.pack()
    
    # Label doleva
    portlabel = tk.Label(button_frame, text="Port(5 nums):")
    portlabel.pack()
    
    # Entry (vstupní pole) vedle labelu
    port_entry = tk.Entry(button_frame)
    port_entry.pack()
    
    
    
    nlabel = tk.Label(button_frame, text="")
    nlabel.pack()
    
    zpet_button = ttk.Button(button_frame, text="Zpět", command=zpet)
    zpet_button.pack(side='left', padx=10)
    
    pokracovat2_button = ttk.Button(button_frame, text="Pokračovat", command=created_join)
    pokracovat2_button.pack(side='left', padx=10)



def handle_client(client_socket, client_address):
    try:
        device_name = socket.gethostbyaddr(client_address[0])[0]
    except socket.herror:
        device_name = "Neznámé zařízení"
    messagebox.showinfo("Nové připojení", f"Připojení od: {device_name}, {client_address[0]}")



def created_join():
    global ip, port_entry, sip_entry, sp_entry, server_socket
    port = port_entry.get()
    
    
    if port == "":
        messagebox.showwarning("Potvrďte data", "Potvrďte port zmáčknutím klávesy enter")
    else:
        
        for widget in button_frame.winfo_children():
            widget.pack_forget()

        cslabel = tk.Label(button_frame, text=f"Creating server")
        cslabel.pack()

        # Vytvoření instance TCP socketu
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Přiřazení IP adresy a portu
        server_address = (str(ip), int(port))
        # Navázání spojení na zadané adrese a portu
        server_socket.bind(server_address)
        # Poslouchání na příchozí spojení
        server_socket.listen()



        for widget in button_frame.winfo_children():
            widget.pack_forget()

        sclabel = tk.Label(button_frame, text=f"server created")
        sclabel.pack()
        time.sleep(3)

        for widget in button_frame.winfo_children():
            widget.pack_forget()

        iplabel = tk.Label(button_frame, text=f"Ip: {ip}")
        iplabel.pack()

        portlabel = tk.Label(button_frame, text=f"Port: {port}")
        portlabel.pack()
        
        nlabel = tk.Label(button_frame, text="")
        nlabel.pack()
        
        siplabel = tk.Label(button_frame, text="Ip serveru:")
        siplabel.pack()
        
        sip_entry = tk.Entry(button_frame)
        sip_entry.pack()

        siplabel = tk.Label(button_frame, text="Port serveru:")
        siplabel.pack()

        sp_entry = tk.Entry(button_frame)
        sp_entry.pack()
        
        nlabel = tk.Label(button_frame, text="")
        nlabel.pack()
        
        domu_button = ttk.Button(button_frame, text="Domů", command=zpetak)
        domu_button.pack(side='left', padx=10)

        pokracovat3_button = ttk.Button(button_frame, text="Pokračovat", command=finally_join)
        pokracovat3_button.pack(side='left', padx=10)
        
        
def finally_join():
    global stavlabel
    
    for widget in button_frame.winfo_children():
            widget.pack_forget()
            
    stavlabel = tk.Label(button_frame, text="-")
    stavlabel.pack()
    
    domu_button = ttk.Button(button_frame, text="Vyčkat na připojení", command=wfc)
    domu_button.pack(side='left', padx=10)

    pokracovat3_button = ttk.Button(button_frame, text="Připojit se", command=connect)
    pokracovat3_button.pack(side='left', padx=10)

def wfc():
    global server_socket, stavlabel, sc, cts, client_socket
    
    if sc == True:
        stavlabel.config(text="Už připojeno")
    else:
    
        stavlabel.config(text="Čekání na připojení")

        # Přijetí připojení
        client_socket, client_address = server_socket.accept()
        # Vytvoření vlákna pro obsluhu klienta
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()

        sc = True

        stavlabel.config(text="Připojeno")
        time.sleep(3)
        stavlabel.config(text="-")
        
    if cts == True and sc == True:
        ls()

def connect():
    global sp_entry, sip_entry, stavlabel, cts, sc, sp, sip
    sp = sp_entry.get()
    sip =  sip_entry.get()
    
    if cts == True:
        stavlabel.config(text="Už připojeno")
    else:
    
        stavlabel.config(text="Připojuji")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((str(sip), int(sp)))

        cts = True

        stavlabel.config(text="Připojeno")
        time.sleep(3)
        stavlabel.config(text="-")
        
    if cts == True and sc == True:
        ls()
    
    
def ls():
    global stavlabel
    
    for widget in button_frame.winfo_children():
        widget.pack_forget()
            
    stavlabel = tk.Label(button_frame, text="-")
    stavlabel.pack()
    
    domu_button = ttk.Button(button_frame, text="Vyčkat na poslání", command=wfs)
    domu_button.pack(side='left', padx=10)

    pokracovat3_button = ttk.Button(button_frame, text="Poslat", command=send)
    pokracovat3_button.pack(side='left', padx=10)

def wfs():
    global server_socket

    # Přijetí připojení
    client_socket, client_address = server_socket.accept()
    # Vytvoření vlákna pro obsluhu klienta
    client_thread = threading.Thread(target=download)
    client_thread.daemon = True
    client_thread.start()

def download():
    messagebox.showinfo("Stahování", "Připojené zařízení začalo odesílat soubor")
    
    try:
        # Přijetí názvu souboru (včetně přípony)
        file_name_with_extension = server_socket.recv(1024)
        if not file_name_with_extension:
            return

        # Dekódování názvu souboru z bytů na řetězec
        file_name = file_name_with_extension.decode()

        # Zpráva o přijímání souboru
        stavlabel.config(text=f"Přijímání souboru: {file_name}")

        # Přijetí dat souboru
        data = client_socket.recv(9999)
        if not data:
            return

        # Uložení souboru
        with open(file_name, "wb") as file:
            file.write(data)

        # Zpráva o úspěšném přijetí souboru
        stavlabel.config(text=f"Přijat soubor: {file_name}")
        time.sleep(3)
        stavlabel.config(text="-")

    except Exception as e:
        messagebox.showerror("Nastala chyba", f"Nastala chyba s připojením: {e}")


def is_android():
    # Kontrola existence souboru /system/build.prop, který je specifický pro Android
    return os.path.exists('/system/build.prop')
    
def send():
    global server_socket, sip, sp
    platform = sys.platform



    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((str(sip), int(sp)))

    if platform.startswith('linux'):
        if is_android():
            try:
                from kivy.uix.filechooser import FileChooserListView
                from kivy.app import App
            except:
                messagebox.showerror("Chyba", "Nešla importovat knihovna kivy")
            
            class FileChooserApp(App):
                selected_file_path = ""  # Proměnná pro uložení cesty k vybranému souboru

                def build(self):
                    file_chooser = FileChooserListView()
                    file_chooser.bind(on_submit=self.on_file_selected)  # Připojení obsluhy události výběru souboru
                    return file_chooser

                def on_file_selected(self, instance, selection):
                    if selection:
                        self.selected_file_path = selection[0]  # Uložení cesty k vybranému souboru

            FileChooserApp().run()
            
        else:
            file_path = filedialog.askopenfilename()
    elif platform == 'win32':
        file_path = filedialog.askopenfilename()
    elif platform == 'darwin':
        file_path = filedialog.askopenfilename()
    else:
        messagebox.showerror("Chyba", "Nešla rozpoznat platforma, na které běží tato aplikace")



    # Získání názvu souboru z cesty
    file_name = file_path.split("/")[-1]

    # Odeslání názvu souboru na server
    client_socket.send(file_name.encode())

    # Otevření a odeslání obsahu souboru na server
    with open(file_path, 'rb') as file:
        data = file.read(9999)
        while data:
            server_socket.send(data)
            data = file.read(9999)

    server_socket.close()


def stop():
    window.destroy()

def zpet():
    for widget in button_frame.winfo_children():
        widget.pack_forget()
    ndps = tk.Label(button_frame, text="File transformer 3000\n")
    ndps.pack()

    Odejit_button = ttk.Button(button_frame, text="Odejít", command=stop)
    Odejit_button.pack(side='left', padx=10)

    pokracovat_button = ttk.Button(button_frame, text="Pokračovat", command=create_server)
    pokracovat_button.pack(side='left', padx=10)


def zpetak():
    server_socket.close()
    # Zabití vláken
    os._exit(0)
    
    for widget in button_frame.winfo_children():
        widget.pack_forget()
    ndps = tk.Label(button_frame, text="File transformer 3000\n")
    ndps.pack()

    Odejit_button = ttk.Button(button_frame, text="Odejít", command=stop)
    Odejit_button.pack(side='left', padx=10)

    pokracovat_button = ttk.Button(button_frame, text="Pokračovat", command=create_server)
    pokracovat_button.pack(side='left', padx=10)




button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

ndps = tk.Label(button_frame, text="File transformer 3000\n")
ndps.pack()

Odejit_button = ttk.Button(button_frame, text="Odejít", command=stop)
Odejit_button.pack(side='left', padx=10)

pokracovat_button = ttk.Button(button_frame, text="Pokračovat", command=create_server)
pokracovat_button.pack(side='left', padx=10)

window.mainloop()
