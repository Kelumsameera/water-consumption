import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException

IP_ADDRESS = "192.168.0.16"
PORT = 502          # Modbus TCP default
SLAVE_ID = 1        # FY600 device ID


async def read_fy600_tcp():
    client = AsyncModbusTcpClient(
        host=IP_ADDRESS,
        port=PORT,
        timeout=2
    )

    await client.connect()

    if not client.connected:
        print("❌ Not connected to FY600 (Modbus TCP)")
        return

    print("✅ Connected to FY600 via Modbus TCP")

    try:
        while True:
            try:
                # -----------------------------
                # READ PV (Process Value)
                # Input Register 0x008A
                # -----------------------------
                pv = await client.read_input_registers(
                    address=0x008A,
                    count=1,
                    slave=SLAVE_ID
                )

                if not pv.isError():
                    print("PV:", pv.registers[0] / 10)
                else:
                    print("❌ PV read error")

                # -----------------------------
                # READ SV (Set Value)
                # Holding Register 0x0000
                # -----------------------------
                sv = await client.read_holding_registers(
                    address=0x0000,
                    count=1,
                    slave=SLAVE_ID
                )

                if not sv.isError():
                    print("SV:", sv.registers[0] / 10)
                else:
                    print("❌ SV read error")

                # -----------------------------
                # READ OUTPUT %
                # Input Register 0x0087
                # -----------------------------
                outp = await client.read_input_registers(
                    address=0x0087,
                    count=1,
                    slave=SLAVE_ID
                )

                if not outp.isError():
                    print("OUTPUT %:", outp.registers[0] / 10)
                else:
                    print("❌ Output read error")

            except ModbusIOException as e:
                print("❌ Modbus IO Error:", e)

            await asyncio.sleep(1)  # polling interval

    finally:
        await client.close()
        print("🔌 Connection closed")


if __name__ == "__main__":
    asyncio.run(read_fy600_tcp())
