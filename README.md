# PowerView BLE Direct Control

This project lets you directly control Hunter Douglas PowerView Gen 3 shades using Bluetooth from your computer. It does not require a hub or Home Assistant. You connect to each blind individually, send a command to move it to a specific position.

This is if you want quick control, want to test your shades, or don’t want to set up a full smart home system.

## What’s Included

There are two Python scripts in this repo:

1. `extract_keys.py`: This script finds nearby shades over Bluetooth and prints out their BLE names. It’s also based on code written by another developer (see credits below).
2. `test_blind.py`: This script connects to one shade and tells it to move to a certain position, like 50%.

## How This Is Different from Home Assistant

Most people use the [hdpv_ble](https://github.com/patman15/hdpv_ble) integration to control their PowerView shades through Home Assistant. That setup is great for full home automation and works through the Home Assistant dashboard. But this repo is different. It talks directly to each blind using Python code, without needing anything else in between.

That means:

- No Home Assistant required
- Allows you to debug issues
- No hub required
- No configuration files beyond these two scripts
- You connect to each blind from your laptop one at a time

## How it Works
- Each shade has a 16‑byte “home key.” Commands are 16‑byte frames encrypted with AES‑ECB using that key and written to a writable GATT characteristic. The shade decrypts and executes (e.g. move to a position).

## How to Use This

### Step 1: Install Dependencies

First, you’ll need to install a couple of Python packages.

Run this in your terminal:

```bash
pip install bleak pycryptodome
```



### Step 2: Put a Shade Into Pairing Mode

Press and hold the shade’s manual/program button until the LED enters pairing mode (flashing pattern specific to your model). Only one controller should be connected; close the PowerView app or disconnect the hub if necessary.



### Step 3: Extract BLE Name and Home Key

Run the key extraction script:

```bash
python extract_keys.py
```

Example output line:

```yaml
Shade 'Left 1':
	BLE name: 'SKL:95F6'
	HomeKey: 4b26434748e662bf9beb185a85dc3b5a
```
Record the BLE name and the 32‑character hex home key for each shade you want to control.



### Step 4: Configure test_blind.py

Open test_blind.py and set:

```python
TARGET_BLE_NAME = "SKL:95F6"
HOMEKEY_HEX = "4b26434748e662bf9beb185a85dc3b5a"
TARGET_POSITION = 0  # 0 = closed, 100 = open
```



### Step 5: Run the Control Script

Execute:

```bash
python test_blind.py
```

Expected behavior: the script scans, connects, writes the encrypted command; the shade LED flashes (e.g., green then blue) and the shade moves to the target position.



### Step 6: Repeat for Additional Shades

Re‑enter pairing mode on another shade, update TARGET_BLE_NAME (and HOMEKEY_HEX if different), and rerun:

```bash
python test_blind.py
```

### Optional: Sequential Control of Multiple Shades

Create a list in a modified script:

```python
shades = [
    {"name": "SKL:95F6", "key": "4b26434748e662bf9beb185a85dc3b5a", "pos": 50},
    {"name": "FAB:D50D", "key": "4b26434748e662bf9beb185a85dc3b5a", "pos": 20},
]
```

Loop over the list, connecting and sending a command to each shade in turn.


### Troubleshooting

| Issue                         | Likely Cause                        | Resolution / Action |
|------------------------------|-------------------------------------|---------------------|
| Shade not found              | Not in pairing mode / out of range  | Re‑enter pairing mode; move closer; ensure only one controller. |
| ATT error 253 on write       | Shade rejected state / busy         | Power cycle shade; re‑enter pairing mode; retry after a short delay. |
| “Data must be aligned” error | Payload not exactly 16 bytes        | Pad raw frame to 16 bytes before AES encryption. |
| LED flashes, no movement     | Command frame not accepted          | Verify command bytes; confirm correct position field; recheck key. |
| Immediate disconnect         | Another device (hub/app) connected  | Close PowerView app; power down hub; ensure exclusive access. |
| No shades respond            | Incorrect home key                  | Re‑extract key; confirm hex string accuracy (32 hex chars). |
| Works once, then fails       | Shade left pairing / timing out     | Re‑enter pairing mode each session; reduce delay between scan and write. |
| Intermittent discovery       | BLE interference / weak signal      | Reduce distance; remove obstacles; try a USB BLE adapter with extension. |
| Wrong shade moves            | Misidentified BLE name              | Re‑run extraction; label shades; double‑check `TARGET_BLE_NAME`. |
| Slow sequential control      | Single adapter handling all links   | Accept sequential nature or script a loop; add additional adapters if needed. |


