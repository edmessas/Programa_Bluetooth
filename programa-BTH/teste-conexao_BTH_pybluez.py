import bluetooth
import tkinter as tk
from tkinter import messagebox
import time

def show_popup(device_name, device_address):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    resposta = messagebox.askquestion("Novo Dispositivo Quer Se Conectar", f"{device_name} ({device_address}) está tentando se conectar!")
    if resposta == "sim": # possível melhoria
        pass
    else:
        pass
    root.destroy()

def monitor_connections(interval=5):
    connected_devices = set()
    
    while True:
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        current_devices = set((addr, name) for addr, name in nearby_devices)
        
        new_devices = current_devices - connected_devices
        
        for addr, name in new_devices:
            show_popup(name, addr)
        
        connected_devices = current_devices ##Erro
        time.sleep(interval)
        print(connected_devices)

# Inicia o monitoramento
monitor_connections()
