import pymem
import pymem.process
import keyboard
import time
from pynput.mouse import Button, Controller
import ctypes as ct
from ctypes import wintypes as wt
from win32gui import GetWindowText, GetForegroundWindow
from random import uniform
from offsets import *

client = Client()
mouse = Controller()
dwEntityList = client.offset('dwEntityList')
dwLocalPlayerPawn = client.offset('dwLocalPlayerPawn')
m_iIDEntIndex = client.get('C_CSPlayerPawnBase', 'm_iIDEntIndex')
m_iTeamNum = client.get('C_BaseEntity', 'm_iTeamNum')
m_iHealth = client.get('C_BaseEntity', 'm_iHealth')
user32 = ct.WinDLL("User32.dll")
GetKeyState = user32.GetKeyState
GetKeyState.argtypes = (ct.c_int,)
GetKeyState.restype = wt.USHORT

triggerKey = 0x10  # Default key is 'Shift'. Refer to https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
with open('settings.ini', 'r') as f:
    triggerKey = int(f.readline(), 16)


def is_key_pressed(virtual_key_code):
    return bool(GetKeyState(virtual_key_code) >> 15)


def main():
    print(f"[-] TriggerBot started.\n[-] Trigger key: {str(triggerKey).upper()}")
    pm = pymem.Pymem("cs2.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                continue

            if is_key_pressed(triggerKey):
                player = pm.read_longlong(client + dwLocalPlayerPawn)
                entityId = pm.read_int(player + m_iIDEntIndex)

                if entityId > 0:
                    entList = pm.read_longlong(client + dwEntityList)

                    entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                    entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                    entityTeam = pm.read_int(entity + m_iTeamNum)
                    playerTeam = pm.read_int(player + m_iTeamNum)

                    if entityTeam != playerTeam:
                        entityHp = pm.read_int(entity + m_iHealth)
                        if entityHp>0:
                            time.sleep(uniform(0.01, 0.03))
                            mouse.press(Button.left)
                            time.sleep(uniform(0.01, 0.05))
                            mouse.release(Button.left)

                time.sleep(0.03)
            else:
                time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except:
            pass

if __name__ == '__main__':
    main()