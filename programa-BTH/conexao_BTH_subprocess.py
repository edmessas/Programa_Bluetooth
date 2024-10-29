import time
import tkinter as tk
from tkinter import messagebox
import subprocess

# Função que cria um pop-up para aceitar ou recusar a conexão
def show_popup(device_name):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    response = False
    
    resposta = messagebox.askyesno(f"{device_name} Tentando Se Conectar", f"{device_name} está tentando se conectar!\n\nDeseja aceitar a conexão?")
    if resposta:
        response = True
    root.destroy()
    return response

# Função para verificar dispositivos Bluetooth emparelhados e conectados no Windows
def get_connected_bluetooth_devices():
    # Comando PowerShell para listar dispositivos Bluetooth emparelhados e conectados
    command = 'powershell "Get-PnpDevice -Class Bluetooth -Status OK | Where-Object { $_.InstanceId -match \'^BTH\' }"'

    # Executa o comando PowerShell
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Lista de dispositivos conectados (nome e ID)
    devices = []

    if result.returncode == 0:
        # Processa a saída para extrair o nome e o ID dos dispositivos
        for line in result.stdout.splitlines():
            if line.strip() and not line.startswith("Status"):  # Ignora o cabeçalho
                parts = line.split()
                if len(parts) > 1:
                    device_id = parts[-1]  # Nome do dispositivo
                    device_name = " ".join(parts[0:-1])  # Combina o restante como nome
                    devices.append((device_name, device_id))
    else:
        print(f"Erro ao obter dispositivos conectados: {result.stderr}")

    return devices

# Função para rejeitar a conexão de um dispositivo Bluetooth
def reject_bluetooth_connection(device_name):
    # Comando PowerShell para desconectar o dispositivo Bluetooth
    command = f'powershell "Get-PnpDevice -Class Bluetooth | Where-Object {{ $_.FriendlyName -eq \'{device_name}\' }} | Disable-PnpDevice -Confirm:$false"'

    try:
        # Executa o comando PowerShell
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Verifica se houve algum erro
        if result.returncode != 0:
            print('Erro ao tentar desconectar o dispositivo:', result.stderr)
        else:
            print('Dispositivo desconectado com sucesso.', result.stdout)
    except Exception as e:
        print(f'Falha ao executar o comando: {e}')

# Função principal para monitorar conexões e perguntar ao usuário
def monitor_bluetooth_connections():
    previous_connected_devices = set()

    while True:
        # Obtém os dispositivos atualmente conectados (nome e ID)
        current_connected_devices = set(get_connected_bluetooth_devices())

        # Verifica se há novos dispositivos tentando se conectar
        new_devices = current_connected_devices - previous_connected_devices

        for device_name, device_id in new_devices:
            print(f"Novo dispositivo detectado: {device_name} ({device_id})")
            # Exibe um pop-up para aceitar ou rejeitar a conexão
            if show_popup(device_name):
                print(f"Conexão com {device_name} aceita.")
            else:
                print(f"Conexão com {device_name} rejeitada.")
                reject_bluetooth_connection(device_name)

        # Atualiza o estado anterior dos dispositivos conectados
        previous_connected_devices = current_connected_devices
        # Espera antes de verificar novamente
        time.sleep(5)

if __name__ == "__main__":
    monitor_bluetooth_connections()
