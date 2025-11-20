#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <DHT.h>

// Configuración LoRaWAN - OTAA (Over The Air Activation)
// Estos valores deben obtenerse de su Network Server (TTN, ChirpStack, etc.)

// Application EUI (LSB format)
static const u1_t PROGMEM APPEUI[8] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}

// Device EUI (LSB format)
static const u1_t PROGMEM DEVEUI[8] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 };
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}

// App Key (MSB format)
static const u1_t PROGMEM APPKEY[16] = { 
  0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
  0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C
};
void os_getDevKey (u1_t* buf) { memcpy_P(buf, APPKEY, 16);}

// Payload que se enviará
static uint8_t payload[8];
static osjob_t sendjob;

// Intervalo de transmisión (segundos)
const unsigned TX_INTERVAL = 60;

// Pin mapping para Arduino
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 9,
    .dio = {2, 3, LMIC_UNUSED_PIN},
};

// Configuración del sensor DHT22
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    Serial.println(F("LoRaWAN Node Starting..."));
    
    // Inicializar sensor
    dht.begin();
    
    // Inicializar LMIC
    os_init();
    LMIC_reset();
    
    // Configurar región (EU868, US915, etc.)
    LMIC_selectSubBand(1); // Para US915
    
    // Configurar Data Rate
    LMIC_setDrTxpow(DR_SF7, 14);
    
    // Configurar Link Check
    LMIC_setLinkCheckMode(0);
    
    // Iniciar join OTAA
    LMIC_startJoining();
    
    Serial.println(F("Intentando JOIN a la red LoRaWAN..."));
}

void onEvent (ev_t ev) {
    Serial.print(os_getTime());
    Serial.print(": ");
    
    switch(ev) {
        case EV_JOINING:
            Serial.println(F("EV_JOINING"));
            break;
            
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));
            {
              u4_t netid = 0;
              devaddr_t devaddr = 0;
              u1_t nwkKey[16];
              u1_t artKey[16];
              LMIC_getSessionKeys(&netid, &devaddr, nwkKey, artKey);
              
              Serial.print("NetID: ");
              Serial.println(netid, DEC);
              Serial.print("DevAddr: ");
              Serial.println(devaddr, HEX);
              
              // Disable link check validation
              LMIC_setLinkCheckMode(0);
              
              // Enviar primer paquete
              do_send(&sendjob);
            }
            break;
            
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED"));
            break;
            
        case EV_REJOIN_FAILED:
            Serial.println(F("EV_REJOIN_FAILED"));
            break;
            
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE (incluye espera de ventanas de recepción)"));
            
            if (LMIC.txrxFlags & TXRX_ACK)
              Serial.println(F("ACK recibido"));
              
            if (LMIC.dataLen) {
              Serial.print(F("Datos recibidos: "));
              Serial.write(LMIC.frame+LMIC.dataBeg, LMIC.dataLen);
              Serial.println();
            }
            
            // Programar siguiente transmisión
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
            break;
            
        case EV_TXSTART:
            Serial.println(F("EV_TXSTART"));
            break;
            
        default:
            Serial.print(F("Evento desconocido: "));
            Serial.println((unsigned) ev);
            break;
    }
}

void do_send(osjob_t* j) {
    // Verificar si hay un trabajo TX/RX pendiente
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, no se envía"));
    } else {
        // Leer sensores
        float temperature = dht.readTemperature();
        float humidity = dht.readHumidity();
        
        Serial.print(F("Temperatura: "));
        Serial.print(temperature);
        Serial.print(F("°C, Humedad: "));
        Serial.print(humidity);
        Serial.println(F("%"));
        
        // Preparar payload
        // Formato: [temp_int][temp_dec][hum_int][hum_dec][battery][status]
        
        int16_t temp_encoded = (int16_t)(temperature * 100);
        uint16_t hum_encoded = (uint16_t)(humidity * 100);
        uint16_t battery = analogRead(A0); // Lectura de batería
        
        payload[0] = (temp_encoded >> 8) & 0xFF;
        payload[1] = temp_encoded & 0xFF;
        payload[2] = (hum_encoded >> 8) & 0xFF;
        payload[3] = hum_encoded & 0xFF;
        payload[4] = (battery >> 8) & 0xFF;
        payload[5] = battery & 0xFF;
        payload[6] = 0x01; // Status byte
        payload[7] = 0x00; // Reservado
        
        // Enviar paquete
        LMIC_setTxData2(1, payload, sizeof(payload), 0);
        Serial.println(F("Paquete en cola para transmisión"));
    }
}

void loop() {
    os_runloop_once();
}