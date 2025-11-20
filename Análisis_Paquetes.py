import struct
import binascii

class LoRaWANPacketAnalyzer:
    def __init__(self):
        self.packet_history = []
        self.suspicious_patterns = []
    
    def parse_lorawan_packet(self, raw_packet):
        """Analiza estructura de paquete LoRaWAN"""
        try:
            # MHDR (1 byte)
            mhdr = raw_packet[0]
            mtype = (mhdr >> 5) & 0x07
            
            packet_types = {
                0: "Join Request",
                1: "Join Accept",
                2: "Unconfirmed Data Up",
                3: "Unconfirmed Data Down",
                4: "Confirmed Data Up",
                5: "Confirmed Data Down"
            }
            
            print(f"\n[PACKET ANALYSIS]")
            print(f"Tipo: {packet_types.get(mtype, 'Unknown')}")
            print(f"MHDR: 0x{mhdr:02X}")
            
            # DevAddr (4 bytes)
            if mtype in [2, 3, 4, 5]:
                dev_addr = struct.unpack('<I', raw_packet[1:5])[0]
                print(f"DevAddr: 0x{dev_addr:08X}")
                
                # FCtrl (1 byte)
                fctrl = raw_packet[5]
                adr = (fctrl >> 7) & 0x01
                adr_ack_req = (fctrl >> 6) & 0x01
                ack = (fctrl >> 5) & 0x01
                fpending = (fctrl >> 4) & 0x01
                
                print(f"ADR: {adr}, ACK: {ack}, FPending: {fpending}")
                
                # Frame Counter (2 bytes)
                fcnt = struct.unpack('<H', raw_packet[6:8])[0]
                print(f"Frame Counter: {fcnt}")
                
                # Verificar anomalías
                self.detect_anomalies(dev_addr, fcnt, mtype)
            
            return True
        
        except Exception as e:
            print(f"Error al analizar paquete: {e}")
            return False
    
    def detect_anomalies(self, dev_addr, fcnt, mtype):
        """Detecta comportamientos anómalos"""
        
        # Verificar reset de frame counter
        if self.packet_history:
            last_fcnt = self.packet_history[-1].get('fcnt', 0)
            if fcnt < last_fcnt:
                print("  ⚠ [ALERTA] Frame counter reset detectado!")
                self.suspicious_patterns.append({
                    'type': 'Frame Counter Reset',
                    'dev_addr': dev_addr,
                    'old_fcnt': last_fcnt,
                    'new_fcnt': fcnt
                })
        
        # Verificar tasa de transmisión anormal
        if len(self.packet_history) > 10:
            recent_packets = self.packet_history[-10:]
            same_device = [p for p in recent_packets if p['dev_addr'] == dev_addr]
            if len(same_device) > 8:
                print("  ⚠ [ALERTA] Tasa de transmisión anormalmente alta!")
        
        # Almacenar en historial
        self.packet_history.append({
            'dev_addr': dev_addr,
            'fcnt': fcnt,
            'mtype': mtype
        })
    
    def check_replay_attack(self, packet_signature):
        """Detecta posibles ataques de repetición"""
        if packet_signature in [p.get('signature') for p in self.packet_history]:
            print("  ⚠ [CRÍTICO] Posible replay attack detectado!")
            return True
        return False

# Ejemplo de uso
if __name__ == "__main__":
    analyzer = LoRaWANPacketAnalyzer()
    
    # Paquetes de ejemplo (simulados)
    example_packets = [
        bytes.fromhex("40F17ABF2600000001AFBF"),
        bytes.fromhex("40F17ABF2600010001AFBF"),
        bytes.fromhex("40F17ABF2600020001AFBF"),
        bytes.fromhex("40F17ABF2600000001AFBF"),  # Frame counter reset
    ]
    
    print("Analizando tráfico LoRaWAN...")
    for i, packet in enumerate(example_packets):
        print(f"\n--- Paquete {i+1} ---")
        analyzer.parse_lorawan_packet(packet)
    
    print(f"\n\nPatrones sospechosos detectados: {len(analyzer.suspicious_patterns)}")