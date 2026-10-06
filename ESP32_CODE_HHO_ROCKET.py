import machine
import time
import math
import network
import socket
from machine import Pin, I2C, ADC

# ==========================================
# CONFIGURATION & PIN MAPPING
# ==========================================
# I2C Display (U2 SSD1306_OLED_I2C)
I2C_SDA_PIN = 8
I2C_SCL_PIN = 9

# NTC Thermistors (R1, R2, R3)
ADC1_PIN = 1  # HHO Generator Temp
ADC2_PIN = 2  # Rocket Nozzle Temp
ADC3_PIN = 3  # Electronics / Circuit Temp

# Relays (via Optoisolators U4, U5)
RL1_PIN = 10  # Relay 1 (e.g., Ignition)
RL2_PIN = 11  # Relay 2 (e.g., HHO Power)

# Safety Thresholds (Celsius)
MAX_HHO_TEMP = 60.0
MAX_NOZZLE_TEMP = 80.0
MAX_ELEC_TEMP = 70.0

# Wi-Fi Credentials for Remote Monitoring
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# ==========================================
# HARDWARE INITIALIZATION
# ==========================================
# Initialize I2C and OLED (Make sure ssd1306.py is uploaded)
try:
    i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)
    import ssd1306
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled_available = True
except Exception as e:
    print("OLED Init Error:", e)
    oled_available = False

# Initialize ADC for NTCs
adc1 = ADC(Pin(ADC1_PIN))
adc2 = ADC(Pin(ADC2_PIN))
adc3 = ADC(Pin(ADC3_PIN))
for adc in (adc1, adc2, adc3):
    adc.atten(ADC.ATTN_11DB)  # Full range 0-3.3V

# Initialize Relays (Assuming Active LOW relay module, set to 1 for OFF)
relay1 = Pin(RL1_PIN, Pin.OUT)
relay2 = Pin(RL2_PIN, Pin.OUT)
relay1.value(1) # OFF
relay2.value(1) # OFF

system_armed = False
emergency_stopped = False

# ==========================================
# TEMPERATURE CALCULATION (NTC Beta Equation)
# ==========================================
def read_ntc_temp(adc_pin, B=3950, R0=10000, T0=298.15, R_series=10000):
    """Reads ADC and converts to Celsius using Beta equation."""
    try:
        val = adc_pin.read_u16() # 0 - 65535
        V_out = val * 3.3 / 65535.0
        
        # Prevent divide by zero
        if V_out >= 3.3: return 999.0
        if V_out <= 0: return -273.15
        
        # Calculate NTC resistance
        R_ntc = (R_series * V_out) / (3.3 - V_out)
        
        # Steinhart-Hart simplified (Beta equation)
        temp_k = 1.0 / ((1.0 / T0) + (1.0 / B) * math.log(R_ntc / R0))
        return temp_k - 273.15
    except Exception as e:
        print("ADC Read Error:", e)
        return 999.0 # Fail-safe high temp reading

# ==========================================
# SAFETY & CONTROL FUNCTIONS
# ==========================================
def emergency_shutdown(reason):
    global system_armed, emergency_stopped
    system_armed = False
    emergency_stopped = True
    relay1.value(1) # Turn OFF Ignition
    relay2.value(1) # Turn OFF HHO Power
    print(f"!!! EMERGENCY SHUTDOWN: {reason} !!!")
    if oled_available:
        oled.fill(0)
        oled.text("!!! DANGER !!!", 0, 0)
        oled.text("EMERGENCY STOP", 0, 20)
        oled.text(reason, 0, 40)
        oled.show()

def check_safety(t_hho, t_nozzle, t_elec):
    if emergency_stopped:
        return False
    if t_hho > MAX_HHO_TEMP:
        emergency_shutdown("HHO OVERHEAT")
        return False
    if t_nozzle > MAX_NOZZLE_TEMP:
        emergency_shutdown("NOZZLE OVERHEAT")
        return False
    if t_elec > MAX_ELEC_TEMP:
        emergency_shutdown("ELEC OVERHEAT")
        return False
    return True

def update_display(t_hho, t_nozzle, t_elec):
    if not oled_available: return
    oled.fill(0)
    oled.text("HHO ROCKET MONITOR", 0, 0)
    oled.text(f"HHO:    {t_hho:.1f} C", 0, 15)
    oled.text(f"NOZZLE: {t_nozzle:.1f} C", 0, 25)
    oled.text(f"ELEC:   {t_elec:.1f} C", 0, 35)
    
    status = "ARMED" if system_armed else "SAFE"
    if emergency_stopped: status = "EMERGENCY"
    oled.text(f"STATUS: {status}", 0, 50)
    oled.show()

# ==========================================
# REMOTE CONTROL (Basic Wi-Fi Socket Server)
# ==========================================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print("Wi-Fi Connected. IP:", wlan.ifconfig()[0])
    else:
        print("Wi-Fi Connection Failed.")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8080))
    s.listen(1)
    s.setblocking(False)
    return s

# ==========================================
# MAIN LOOP
# ==========================================
def main():
    global system_armed, emergency_stopped
    
    print("Initializing HHO Rocket System...")
    connect_wifi()
    server_socket = start_server()
    
    while True:
        # 1. Read Temperatures
        t_hho = read_ntc_temp(adc1)
        t_nozzle = read_ntc_temp(adc2)
        t_elec = read_ntc_temp(adc3)
        
        # 2. Safety Check
        is_safe = check_safety(t_hho, t_nozzle, t_elec)
        
        # 3. Update OLED
        update_display(t_hho, t_nozzle, t_elec)
        
        # 4. Remote Control Handling
        try:
            conn, addr = server_socket.accept()
            print("Client connected from", addr)
            request = conn.recv(1024).decode('utf-8').strip()
            
            if request == "STATUS":
                response = f"T_HHO:{t_hho:.1f},T_NOZ:{t_nozzle:.1f},T_ELEC:{t_elec:.1f},ARMED:{system_armed},EMERG:{emergency_stopped}"
            elif request == "IGNITE" and is_safe:
                system_armed = True
                relay1.value(0) # ON (Active LOW)
                response = "IGNITION ON"
            elif request == "HHO_ON" and is_safe:
                relay2.value(0) # ON (Active LOW)
                response = "HHO POWER ON"
            elif request == "STOP":
                emergency_shutdown("REMOTE COMMAND")
                response = "SYSTEM STOPPED"
            elif request == "RESET":
                if t_hho < MAX_HHO_TEMP and t_nozzle < MAX_NOZZLE_TEMP and t_elec < MAX_ELEC_TEMP:
                    emergency_stopped = False
                    response = "SYSTEM RESET OK"
                else:
                    response = "RESET DENIED: TEMPS HIGH"
            else:
                response = "UNKNOWN COMMAND"
                
            conn.send(response.encode('utf-8'))
            conn.close()
        except OSError:
            pass # No incoming connections
            
        time.sleep(0.5)

if __name__ == "__main__":
    main()