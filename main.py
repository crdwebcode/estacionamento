#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import qrcode
from PIL import Image, ImageTk
import os
import time

# Define a classe principal do aplicativo
class ParkSulApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Park Sul - Gerenciamento de Estacionamento")
        
        # Cria os widgets da interface
        self.create_widgets()
        # Atualiza o status das vagas de estacionamento
        self.update_slots()
    
    def create_widgets(self):
        # Rótulo para a entrada da placa do veículo
        self.plate_label = tk.Label(self.root, text="Placa do Veículo:")
        self.plate_label.grid(row=0, column=0, padx=5, pady=5)
        # Campo de entrada para a placa do veículo
        self.plate_entry = tk.Entry(self.root)
        self.plate_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame para os botões das vagas de estacionamento
        self.slots_frame = tk.Frame(self.root)
        self.slots_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Cria 30 botões representando as vagas de estacionamento
        self.slot_buttons = []
        for i in range(30):
            btn = tk.Button(self.slots_frame, text=f'Vaga {i+1}', width=10, height=2, command=lambda i=i: self.occupy_slot(i+1))
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
            self.slot_buttons.append(btn)
        
        # Rótulo para a contagem de vagas disponíveis
        self.available_label = tk.Label(self.root, text="Vagas Disponíveis: 30")
        self.available_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Rótulo para a entrada da placa do veículo para saída
        self.exit_plate_label = tk.Label(self.root, text="Placa para Saída:")
        self.exit_plate_label.grid(row=3, column=0, padx=5, pady=5)
        # Campo de entrada para a placa do veículo para saída
        self.exit_plate_entry = tk.Entry(self.root)
        self.exit_plate_entry.grid(row=3, column=1, padx=5, pady=5)
        # Botão para registrar a saída do veículo
        self.exit_button = tk.Button(self.root, text="Registrar Saída", command=self.register_exit)
        self.exit_button.grid(row=3, column=2, padx=5, pady=5)
    
    # Função para atualizar o status das vagas
    def update_slots(self):
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute('SELECT slot_id, occupied FROM parking_slots')
        slots = c.fetchall()
        
        available_slots = 0
        for slot_id, occupied in slots:
            if occupied:
                self.slot_buttons[slot_id-1].config(bg='red')
            else:
                self.slot_buttons[slot_id-1].config(bg='green')
                available_slots += 1
        
        self.available_label.config(text=f"Vagas Disponíveis: {available_slots}")
        conn.close()
    
    # Função para ocupar uma vaga
    def occupy_slot(self, slot_id):
        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showerror("Erro", "Por favor, insira a placa do veículo.")
            return
        
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute('SELECT occupied FROM parking_slots WHERE slot_id=?', (slot_id,))
        occupied = c.fetchone()[0]
        
        if occupied:
            messagebox.showerror("Erro", "Esta vaga já está ocupada.")
        else:
            entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('UPDATE parking_slots SET plate=?, entry_time=?, occupied=? WHERE slot_id=?', 
                      (plate, entry_time, True, slot_id))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Veículo {plate} registrado na vaga {slot_id}.")
        
        conn.close()
        self.update_slots()
        self.plate_entry.delete(0, tk.END)
    
    # Função para registrar a saída de um veículo
    def register_exit(self):
        plate = self.exit_plate_entry.get().strip().upper()
        if not plate:
            messagebox.showerror("Erro", "Por favor, insira a placa do veículo para saída.")
            return
        
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute('SELECT slot_id, entry_time FROM parking_slots WHERE plate=? AND occupied=?', (plate, True))
        result = c.fetchone()
        
        if result:
            slot_id, entry_time = result
            exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entry_dt = datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
            exit_dt = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
            duration = (exit_dt - entry_dt).total_seconds() / 3600  # Duração em horas
            
            fee = self.calculate_fee(duration)
            c.execute('INSERT INTO parking_records (plate, entry_time, exit_time, fee) VALUES (?, ?, ?, ?)', 
                      (plate, entry_time, exit_time, fee))
            c.execute('UPDATE parking_slots SET plate=NULL, entry_time=NULL, occupied=? WHERE slot_id=?', 
                      (False, slot_id))
            conn.commit()
            
            self.generate_receipt(plate, entry_time, exit_time, fee)
            messagebox.showinfo("Saída Registrada", f"Veículo {plate} saiu da vaga {slot_id}.")
        else:
            messagebox.showerror("Erro", "Placa não encontrada ou veículo já saiu.")
        
        conn.close()
        self.update_slots()
        self.exit_plate_entry.delete(0, tk.END)
    
    # Função para calcular a tarifa com base na duração
    def calculate_fee(self, duration):
        base_rate = 5.0  # Tarifa base por hora
        return round(duration * base_rate, 2)
    
    # Função para gerar o recibo de pagamento
    def generate_receipt(self, plate, entry_time, exit_time, fee):
        # Gera o QR code para pagamento
        if not os.path.exists('qrcodes'):
            os.makedirs('qrcodes')
        if not os.path.exists('receipts'):
            os.makedirs('receipts')
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Pagamento PIX - Veículo: {plate}, Valor: R${fee}")
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_filename = f"qrcodes/{plate}_{time.time()}.png"
        img.save(img_filename)
        
        # Gera o recibo (implementação básica)
        receipt = f"Recibo de Pagamento\n\nVeículo: {plate}\nEntrada: {entry_time}\nSaída: {exit_time}\nTotal a Pagar: R${fee}\n\n"
        receipt += "Escaneie o QR Code para pagamento via PIX."
        receipt_filename = f"receipts/{plate}_{time.time()}.txt"
        
        with open(receipt_filename, 'w') as file:
            file.write(receipt)
        
        # Exibe o recibo em uma nova janela
        top = tk.Toplevel(self.root)
        top.title("Recibo de Pagamento")
        tk.Label(top, text=receipt).pack(padx=10, pady=10)
        img = Image.open(img_filename)
        img = ImageTk.PhotoImage(img)
        tk.Label(top, image=img).pack(padx=10, pady=10)
        top.mainloop()

# Código principal para executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ParkSulApp(root)
    root.mainloop()
