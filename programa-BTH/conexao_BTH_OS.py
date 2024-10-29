import os
import time
import tkinter as tk
from tkinter import messagebox

# Função que cria um pop-up para aceitar ou recusar a conexão
def show_popup(device_name):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    response = False
    
    resposta = messagebox.askyesno("Novo Dispositivo Quer Se Conectar", f"{device_name}  está tentando se conectar!")
    if resposta:
        response = True
    else:
        pass
    root.destroy()
    return response

# Função para verificar dispositivos emparelhados e conectados
def get_connected_bluetooth_devices():
    # Comando PowerShell para listar dispositivos Bluetooth emparelhados e conectados
    command = 'powershell "Get-PnpDevice -Class Bluetooth -Status OK | Where-Object { $_.InstanceId -match \'^BTH\' }"'
    # Executa o comando e captura a saída
    output = os.popen(command).read()
    
    # Lista de dispositivos conectados
    devices = []

    if output:
        lines = output.strip().split("\n")[2:]  # Remove cabeçalhos
        for line in lines:
            device_info = line.split()
            if len(device_info) > 1:
                devices.append(device_info[-1])  # Nome do dispositivo

    return devices

# Função principal para monitorar conexões e perguntar ao usuário

def reject_bluetooth_connection(device_name):
    # Executa o comando PowerShell para desconectar o dispositivo
    command = f'powershell "Get-PnpDevice -Class Bluetooth | Where-Object {{ $_.FriendlyName -eq \'{device_name}\' }} | Disable-PnpDevice -Confirm:$false"'
    os.system(command)
    return command
def monitor_bluetooth_connections():
    previous_connected_devices = set()

    while True:
        current_connected_devices = set(get_connected_bluetooth_devices()) # Para a ação bash funcionar deve receber MAC address ao invés do nome do Bluetooth

        # Verifica se há novos dispositivos tentando se conectar
        new_devices = current_connected_devices - previous_connected_devices

        for device in new_devices:
            print(f"Novo dispositivo detectado: {device}")
            # Exibe um pop-up para aceitar ou rejeitar a conexão
            if show_popup(device):
                print(f"Conexão com {device} aceita.")
            else:
                print(f"Conexão com {device} rejeitada.")
                reject_bluetooth_connection(device)

        # Atualiza o estado anterior dos dispositivos conectados
        previous_connected_devices = current_connected_devices
        # Espera antes de verificar novamente
        time.sleep(5)

if __name__ == "__main__":
    monitor_bluetooth_connections()