"""
Gateway LoRaWAN básico usando Raspberry Pi + SX1276
Reenvía paquetes a Network Server
"""

import time
import json
import socket
from datetime import datetime

class LoRaWANGateway:
    def __init__(self, server_address, gateway_id):
        self.server_address = server_address
        self.gateway_id = gateway_id
        self.socket = None
        
    def connect_to_server(self):
        """Conecta al Network Server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Gateway {self.gateway_id} conectado al servidor {self.server_address}")
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
    
    def receive_lora_packet(self):
        """Recibe paquetes LoRa del módulo SX1276"""
        # En implementación real, esto vendría del hardware
        # Simulación de paquete recibido
        packet = {
            'timestamp': datetime.now().isoformat(),
            'frequency': 868100000,
            'rssi': -45,
            'snr': 8.5,
            'data': '40F17ABF2600000001AFBF4E4D123456'
        }
        return packet
    
    def forward_to_server(self, packet):
        """Reenvía paquete al Network Server"""
        try:
            # Construir mensaje en formato Semtech UDP
            message = {
                'protocol_version': 2,
                'token': 0x1234,
                'identifier': 0x00,  # PUSH_DATA
                'gateway_id': self.gateway_id,
                'rxpk': [{
                    'time': packet['timestamp'],
                    'tmst': int(time.time() * 1000000),
                    'freq': packet['frequency'] / 1000000,
                    'chan': 0,
                    'rfch': 0,
                    'stat': 1,
                    'modu': 'LORA',
                    'datr': 'SF7BW125',
                    'codr': '4/5',
                    'rssi': packet['rssi'],
                    'lsnr': packet['snr'],
                    'size': len(packet['data']) // 2,
                    'data': packet['data']
                }]
            }
            
            json_data = json.dumps(message)
            print(f"Reenviando paquete: RSSI={packet['rssi']}dBm, SNR={packet['snr']}dB")
            
            # En implementación real enviaría por UDP al servidor
            # self.socket.sendto(json_data.encode(), self.server_address)
            
            return True
        except Exception as e:
            print(f"Error al reenviar: {e}")
            return False
    
    def send_stats(self):
        """Envía estadísticas del gateway al servidor"""
        stats = {
            'gateway_id': self.gateway_id,
            'time': datetime.now().isoformat(),
            'rxnb': 15,  # Paquetes recibidos
            'rxok': 14,  # Paquetes válidos
            'rxfw': 14,  # Paquetes reenviados
            'ackr': 95.0,  # Tasa de ACK
            'temp': 25.5  # Temperatura del gateway
        }
        print(f"Estadísticas: {stats['rxok']}/{stats['rxnb']} paquetes válidos")
        return stats

# Ejecución
if __name__ == "__main__":
    gateway = LoRaWANGateway(
        server_address=('lorawan.example.com', 1700),
        gateway_id='AA555A0000000000'
    )
    
    if gateway.connect_to_server():
        print("Gateway en ejecución...")
        
        # Ciclo principal
        for i in range(5):
            print(f"\n--- Ciclo {i+1} ---")
            packet = gateway.receive_lora_packet()
            gateway.forward_to_server(packet)
            
            if i % 3 == 0:
                gateway.send_stats()
            
            time.sleep(2)