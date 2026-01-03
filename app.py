import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


MODBUS_IP = "192.168.0.16"
MODBUS_PORT = 502
SLAVE_ID = 1

fy600 = {
    "pv": None,
    "sv": None,
    "output": None,
    "status": "disconnected"
}

client: AsyncModbusTcpClient | None = None
read_task: asyncio.Task | None = None
modbus_lock = asyncio.Lock()

# ---------------- READ LOOP ----------------
async def fy600_read_loop():
    global client

    while True:
        try:
            if client is None or not client.connected:
                client = AsyncModbusTcpClient(
                    host=MODBUS_IP,
                    port=MODBUS_PORT,
                    timeout=3
                )
                await client.connect()

            if not client.connected:
                fy600["status"] = "not_connected"
                await asyncio.sleep(3)
                continue

            fy600["status"] = "connected"

            async with modbus_lock:
                pv = await client.read_input_registers(0x008A, 1, slave=SLAVE_ID)
                if not pv.isError():
                    fy600["pv"] = pv.registers[0] 
                    print('PV Register Value:', pv.registers[0])

                sv = await client.read_holding_registers(0x0000, 1, slave=SLAVE_ID)
                if not sv.isError():
                    fy600["sv"] = sv.registers[0] / 10

                outp = await client.read_input_registers(0x0087, 1, slave=SLAVE_ID)
                if not outp.isError():
                    fy600["output"] = outp.registers[0] / 10

            print(
                f"READ → Level:{fy600['pv']}% "
                f"SV:{fy600['sv']} "
                f"OUT:{fy600['output']}%"
            )

        except ModbusIOException as e:
            fy600["status"] = "modbus_error"
            print("❌ Modbus read error:", e)
            if client:
                client.close()
                client = None

        await asyncio.sleep(2)  # IMPORTANT

# ---------------- FASTAPI LIFESPAN ----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global read_task
    print("🚀 API started (READ loop running)")
    read_task = asyncio.create_task(fy600_read_loop())
    yield
    print("🛑 API stopping")
    if read_task:
        read_task.cancel()
    if client:
        client.close()

app = FastAPI(lifespan=lifespan)

# ---------------- READ APIs ----------------
@app.get("/fy600")
async def read_all():
    return fy600

@app.get("/fy600/level")
async def read_level():
    return {"level_percent": fy600["pv"]}

# ---------------- WRITE APIs ----------------
@app.post("/fy600/sv/{value}")
async def set_sv(value: float):
    if not client or not client.connected:
        return {"status": "error"}

    async with modbus_lock:
        await client.write_register(0x0000, int(value * 10), slave=SLAVE_ID)

    return {"status": "ok", "sv": value}

class PID(BaseModel):
    p: float
    i: int
    d: int

@app.post("/fy600/pid")
async def set_pid(pid: PID):
    if not client or not client.connected:
        return {"status": "error"}

    async with modbus_lock:
        await client.write_register(0x0039, int(pid.p * 10), slave=SLAVE_ID)
        await client.write_register(0x003A, pid.i, slave=SLAVE_ID)
        await client.write_register(0x003B, pid.d, slave=SLAVE_ID)

    return {"status": "ok", "pid": pid}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def health():
    return {"status": "up"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
# To run the app: python app.py
