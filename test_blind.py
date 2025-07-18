import asyncio
from bleak import BleakClient, BleakScanner
from Crypto.Cipher import AES
import sys

CHAR_UUID = "cafe1001-c0ff-ee01-8000-a110ca7ab1e0"
TARGET_POSITION = 0
BLINDS = [
    ("Left 1", "SKL:95F6"), ("Left 2", "SKL:3256"), ("Left 3", "SKL:5338"),
    ("Left 4", "SKL:9B25"), ("Left 5", "FAB:D51C"), ("Right 1", "SKL:F5FC"), 
    ("Right 2", "SKL:9C8E"), ("Right 4", "FAB:D50D")
]
HOMEKEY = bytes.fromhex("4b26434748e662bf9beb185a85dc3b5a")

def build_cmd(pos, seq=1):
    p = (pos*100).to_bytes(2, 'little')
    pl = p + bytes([0,128,0,128,0,128,0])
    h = (0x01F7).to_bytes(2,'little') + bytes([seq,len(pl)])
    return h+pl

def encrypt(key, data):
    return AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=bytes(16)).encrypt(data)

async def move_blind(name, ble_name, addr):
    try:
        async with BleakClient(addr) as c:
            await asyncio.sleep(0.2)
            _ = c.services
            evt = asyncio.Event()
            def handler(_, __): evt.set()
            await c.start_notify(CHAR_UUID, handler)
            await c.write_gatt_char(CHAR_UUID, encrypt(HOMEKEY, build_cmd(TARGET_POSITION)), response=False)
            try:
                await asyncio.wait_for(evt.wait(), timeout=5)
                await c.stop_notify(CHAR_UUID)
                return name, True, "Success"
            except:
                await c.stop_notify(CHAR_UUID)
                return name, False, "No response"
    except Exception as e:
        return name, False, str(e)

async def main():
    print("Scanning...")
    found = {d.name: d.address for d in await BleakScanner.discover(timeout=8.0)}
    tasks = [move_blind(n, b, found.get(b)) for n, b in BLINDS if b in found]
    missing = [(n, False, "Not found") for n, b in BLINDS if b not in found]
    results = await asyncio.gather(*tasks) if tasks else []
    print("\nSummary:")
    for n, ok, msg in results+missing:
        print(f"{n}: {'Success' if ok else 'Failed'} - {msg}")

if __name__ == "__main__":
    try:
        pos = int(input("Enter 0 to close or 100 to open all blinds: ").strip())
        if pos not in (0, 100):
            print("Invalid input. Defaulting to 0 (close).")
            pos = 0
    except Exception:
        print("Invalid input. Defaulting to 0 (close).")
        pos = 0
    TARGET_POSITION = pos
    asyncio.run(main())
