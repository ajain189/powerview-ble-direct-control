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
