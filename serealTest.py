from pymodbus.client.serial import ModbusSerialClient

# -----------------------------
# SERIAL CONFIG (FY600)
# -----------------------------
client = ModbusSerialClient(
    port="COM7",        # Windows: COM3 | Linux: /dev/ttyUSB0
    baudrate=9600,
    parity="E",         # FY600 default: Even
    stopbits=1,
    bytesize=8,
    timeout=1
)

SLAVE_ID = 1

client.connect()

# -----------------------------
# READ PROCESS VALUE (PV)
# Register: 0x008A (138)
# -----------------------------
pv = client.read_holding_registers(
    address=0x008A,
    count=1,
    slave=SLAVE_ID
)

if not pv.isError():
    pv_value = pv.registers[0] / 10   # FY600 uses x10 scaling
    print("PV:", pv_value)

# -----------------------------
# READ SET VALUE (SV)
# Register: 0x0000
# -----------------------------
sv = client.read_holding_registers(
    address=0x0000,
    count=1,
    slave=SLAVE_ID
)

if not sv.isError():
    sv_value = sv.registers[0] / 10
    print("SV:", sv_value)

# -----------------------------
# READ OUTPUT %
# Register: 0x0087
# -----------------------------
outp = client.read_holding_registers(
    address=0x0087,
    count=1,
    slave=SLAVE_ID
)

if not outp.isError():
    output_percent = outp.registers[0] / 10
    print("OUTPUT %:", output_percent)

client.close()
