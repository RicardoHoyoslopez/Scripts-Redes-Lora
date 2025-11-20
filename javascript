/**
 * Decoder de Payload para Network Server
 * Decodifica los datos binarios recibidos del nodo
 */

function Decoder(bytes, port) {
  var decoded = {};
  
  if (port === 1) {
    // Decodificar temperatura (2 bytes, signed)
    var temp_raw = (bytes[0] << 8) | bytes[1];
    if (temp_raw > 32767) temp_raw -= 65536;
    decoded.temperature = temp_raw / 100.0;
    
    // Decodificar humedad (2 bytes, unsigned)
    var hum_raw = (bytes[2] << 8) | bytes[3];
    decoded.humidity = hum_raw / 100.0;
    
    // Decodificar batería (2 bytes)
    var battery_raw = (bytes[4] << 8) | bytes[5];
    decoded.battery_voltage = (battery_raw / 1023.0) * 3.3 * 2; // Divisor de voltaje
    
    // Status
    decoded.status = bytes[6];
    
    // Calcular nivel de batería
    if (decoded.battery_voltage > 4.0) {
      decoded.battery_level = 100;
    } else if (decoded.battery_voltage > 3.7) {
      decoded.battery_level = 75;
    } else if (decoded.battery_voltage > 3.4) {
      decoded.battery_level = 50;
    } else if (decoded.battery_voltage > 3.0) {
      decoded.battery_level = 25;
    } else {
      decoded.battery_level = 10;
    }
  }
  
  return decoded;
}

// Ejemplo de uso
var payload = [0x09, 0xC4, 0x19, 0x28, 0x03, 0xFF, 0x01, 0x00];
var decoded = Decoder(payload, 1);

console.log("Datos decodificados:");
console.log("Temperatura: " + decoded.temperature + "°C");
console.log("Humedad: " + decoded.humidity + "%");
console.log("Batería: " + decoded.battery_voltage.toFixed(2) + "V (" + decoded.battery_level + "%)");