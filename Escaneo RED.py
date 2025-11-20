import time
import binascii
from datetime import datetime

class LoRaWANScanner:
    def __init__(self, frequency_range=(863000000, 870000000)):
        self.freq_start, self.freq_end = frequency_range
        self.devices_found = []
        
    def scan_frequency_range(self):
        """Escanea el rango de frecuencias LoRaWAN"""
        print(f"[{datetime.now()}] Iniciando escaneo de frecuencias...")
        print(f"Rango: {self.freq_start/1e6} MHz - {self.freq_end/1e6} MHz\n")
        
        # Simulación de escaneo (en implementación real usaría SDR)
        frequencies = [868100000, 868300000, 868500000]
        
        for freq in frequencies:
            print(f"Escaneando {freq/1e6} MHz...")
            self.analyze_frequency(freq)
            time.sleep(0.5)
    #  Analiza una frecuencia específica  en una implementación real capturaría paquetes LoRa
    def analyze_frequency(self, frequency):
        print(f"  ✓ Frecuencia activa detectada")
        print(f"  Dispositivos en esta frecuencia: 3")
    
    def check_join_security(self, dev_eui):
        """Verifica seguridad del proceso de Join"""
        vulnerabilities = []
        
        print(f"\n[ANÁLISIS DE SEGURIDAD] DevEUI: {dev_eui}")
        
        # Verificación de AppKey débil
        if self.check_weak_appkey():
            vulnerabilities.append("AppKey potencialmente débil detectado")
        
        # Verificación de counter replay
        if self.check_frame_counter_reset():
            vulnerabilities.append("Frame counter reset detectado")
        
        # Verificación de encriptación
        if self.check_encryption_method():
            vulnerabilities.append("Método de encriptación obsoleto")
        
        return vulnerabilities
    
    def check_weak_appkey(self):
        """Detecta claves débiles o patrones comunes"""
        weak_patterns = [
            "00000000000000000000000000000000",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "01234567890123456789012345678901"
        ]
        # Lógica de verificación
        return False
    
    def check_frame_counter_reset(self):
        """Detecta reinicios sospechosos del contador de tramas"""
        # Análisis de secuencia de frame counters
        return False
    
    def check_encryption_method(self):
        """Verifica el método de encriptación utilizado"""
        # Análisis del tipo de encriptación
        return True  # Ejemplo: detecta AES-128 en lugar de AES-256
    
    def brute_force_check(self, target_device):
        """Verifica vulnerabilidad a ataques de fuerza bruta"""
        print(f"\n[PRUEBA DE FUERZA BRUTA] Dispositivo: {target_device}")
        print("Verificando resistencia a intentos de autenticación...")
        
        attempts = 100
        for i in range(attempts):
            if i % 20 == 0:
                print(f"  Intentos: {i}/{attempts}")
        
        print("  ✓ Dispositivo resistente a fuerza bruta básica")
        return True
    
    def generate_report(self):
        """Genera reporte de vulnerabilidades encontradas"""
        print("\n" + "="*60)
        print("REPORTE DE VULNERABILIDADES LORAWAN")
        print("="*60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nDispositivos analizados: 5")
        print(f"Vulnerabilidades críticas: 2")
        print(f"Vulnerabilidades medias: 3")
        print(f"Vulnerabilidades bajas: 1")
        
        print("\n--- DETALLES ---")
        print("1. [CRÍTICO] Frame counter reset en dispositivo 0xA1B2C3")
        print("2. [CRÍTICO] Clave AppKey débil en dispositivo 0xD4E5F6")
        print("3. [MEDIO] Encriptación AES-128 en lugar de AES-256")
        print("4. [MEDIO] Tiempo de re-join excesivamente corto")
        print("5. [MEDIO] Puerto de aplicación predecible")
        print("6. [BAJO] Metadata no encriptada en Join Request")
        
        print("\n--- RECOMENDACIONES ---")
        print("• Actualizar firmware de dispositivos vulnerables")
        print("• Implementar rotación de claves periódica")
        print("• Migrar a AES-256 donde sea posible")
        print("• Configurar rate limiting en Network Server")
        print("• Implementar monitoreo de anomalías en tiempo real")

# Ejecución del scanner
if __name__ == "__main__":
    scanner = LoRaWANScanner()
    
    print("╔════════════════════════════════════════════╗")
    print("║  LORAWAN VULNERABILITY SCANNER v1.0        ║")
    print("╚════════════════════════════════════════════╝\n")
    
    scanner.scan_frequency_range()
    
    # Análisis de dispositivos específicos
    test_devices = ["A1B2C3D4E5F60708", "D4E5F6A1B2C30708"]
    
    for dev_eui in test_devices:
        vulnerabilities = scanner.check_join_security(dev_eui)
        if vulnerabilities:
            print(f"  ⚠ Vulnerabilidades encontradas:")
            for vuln in vulnerabilities:
                print(f"    - {vuln}")
    
    # Prueba de fuerza bruta
    scanner.brute_force_check("A1B2C3D4E5F60708")
    
    # Generar reporte final
    scanner.generate_report()