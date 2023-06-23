import pymem
import pymem.process
import keyboard
from math import sqrt, pi, atan
import math
import time
import mouse
import random
import pyautogui
from csgo import *
import psutil
from os import system
import colorama

system("cls")

art = """

you can sea source in : 'https://github.com/kinite-gp/CSGO-MULTICHEAT-EXTERNAL'
Give us a star if you like

alt + g  >> wallhack
alt + i  >> aimbot
alt + f  >> noflash
alt + r  >> radarcham

You can turn it ON and OFF with the keys

"""

colorama.init()

print(colorama.Fore.BLUE + art + colorama.Fore.RESET)

print(colorama.Fore.RED)

while True:
    for i in psutil.process_iter():
        if "csgo.exe" in i.name():
            break
        else:
            txt = "please open csgo."
            for c in txt:
                if c == ".":
                    print(c)
                    time.sleep(0.2)
                else:
                    time.sleep(0.2)
                    print(c,end="")
                    
print(colorama.Fore.GREEN)

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle,"engine.dll").lpBaseOfDll

aimfov = 120

def normalizeAngles(viewAngleX,viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < 180:
        viewAngleY += 360
    return viewAngleX, viewAngleY

def checkangles(x,y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > -360:
        return False
    elif y < -360:
        return False
    else:
        return True
    
def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True
    
def clac_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
        
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey

def calcangle(localposl, localpos2, localpos3, enemyposl, enemypos2, enemypos3):
    try:
        delta_x = localposl - enemyposl
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x,y
    except:
        pass
 
 
def glow():
    try:
        glow_manager = pm.read_uint(client + dwGlowObjectManager)
        for i in range(1, 32):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)
            if entity > 0:
                entity_team_id = pm.read_uint(entity + m_iTeamNum)
                entity_glow = pm.read_uint(entity + m_iGlowIndex)
    
                if entity_team_id == 3:
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, 1.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, 0.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, 0.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, 0.7)
                    pm.write_bool(glow_manager + entity_glow * 0x38 + 0x28, True)
                    pm.write_bool(glow_manager + entity_glow * 0x38 + 0x29, False)
    
                if entity_team_id == 2:
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, 0.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, 1.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, 0.0)
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, 0.7)
                    pm.write_bool(glow_manager + entity_glow * 0x38 + 0x28, True)
                    pm.write_bool(glow_manager + entity_glow * 0x38 + 0x29, False)
        time.sleep(0.001)
    except Exception as err:
        print(err)
        
def fire_int():
    return range(1,random.randint(1,3))    

def radarcham():
    for i in range(1,32):
                        entity = pm.read_uint(client + dwEntityList + i * 0x10)
                        if entity:
                            pm.write_uint(entity + m_bSpotted, 1)
                            entity_team_id = pm.read_uint(entity + m_iTeamNum)

                            if entity_team_id == 2:
                                pm.write_uint(entity + m_clrRender, 255)
                                pm.write_uint(entity + m_clrRender + 0x1, 51)
                                pm.write_uint(entity + m_clrRender + 0x2, 0)

                            elif entity_team_id == 3:
                                pm.write_uint(entity + m_clrRender, 0)
                                pm.write_uint(entity + m_clrRender + 0x1, 51)
                                pm.write_uint(entity + m_clrRender + 0x2, 255)
                            else:
                                pass

def noflash():
    localPlayer = pm.read_uint(client + dwLocalPlayer)
    if(localPlayer):
        flash_val = (localPlayer + m_flFlashMaxAlpha)
        if flash_val:
            pm.write_uint(flash_val, 1)

def imbot():
    player = pm.read_uint(client + dwLocalPlayer)
    engine_pointer = pm.read_uint(engine + dwClientState)
    localTeam = pm.read_uint(player + m_iTeamNum)
    
    
    target = None
    olddistx = 111111111111
    olddisty = 111111111111
        
    for i in range(1, 32):
        entity = pm.read_uint(client + dwEntityList + i * 0x10)
        if entity:
            try:
                entity_team_id = pm.read_uint(entity + m_iTeamNum)
                entity_hp = pm.read_uint(entity + m_iHealth)
                entity_dormant = pm.read_uint(entity + m_bDormant)
            except:
                print("Finds player info once")
                    
            if localTeam != entity_team_id and entity_hp > 0:
                entity_bones = pm.read_uint(entity + m_dwBoneMatrix)
                localpos_x_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                localpos_Y_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                localpos_z_angles = pm.read_float(player + m_vecViewOffset + 0x8)
                localpos1 = pm.read_float(player + m_vecOrigin)
                localpos2 = pm.read_float(player + m_vecOrigin + 4)
                localpos3 = pm.read_float(player +m_vecOrigin + 8) + localpos_z_angles
                    
                try:
                    entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xc)
                    entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1c)
                    entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2c)
                except:
                    continue
                    
                X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                newdist_x, newdist_y = clac_distance(localpos_x_angles, localpos_Y_angles, X, Y)
                    
                if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= aimfov and newdist_y <= aimfov:
                    olddistx, olddisty = newdist_x, newdist_y
                    target, target_hp, target_dormant = entity, entity_hp, entity_dormant
                        
                    target_x, target_y, target_z = entitypos_x,entitypos_y,entitypos_z
                        
            
            if target and target_hp > 0 and not target_dormant:
                x, y = calcangle(localpos1,localpos2,localpos3,target_x,target_y,target_z)
                normalize_x, normalize_y = normalizeAngles(x,y)
                    
                pm.write_float(engine_pointer + dwClientState_ViewAngles, normalize_x)
                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y)

glow_status = False                  
aimbot_status = False
noflash_status = False
radarcham_status = False




if __name__ == "__main__":
    while True:
        if keyboard.is_pressed("alt"):
            if keyboard.is_pressed("g"):
                if glow_status:
                    print("Wall-Hack Disable!")
                    glow_status = False
                    time.sleep(3)
                else:
                    print("Wall-Hack Enable!")
                    glow_status = True
                    time.sleep(3)
            elif keyboard.is_pressed("i"):
                if aimbot_status:
                    print("Aim-Bot Disable!")
                    aimbot_status = False
                    time.sleep(3)
                else:
                    print("Aim-Bot Enable!")
                    aimbot_status = True
                    time.sleep(3)
            elif keyboard.is_pressed("f"):
                if noflash_status:
                    print("NoFlash Disable!")
                    noflash_status = False
                    time.sleep(3)
                else:
                    print("NoFlash Enable!")
                    noflash_status = True
                    time.sleep(3)
            elif keyboard.is_pressed("r"):
                if radarcham_status:
                    print("RadarCham Disable!")
                    radarcham_status = False
                    time.sleep(3)
                else:
                    print("RadarCham Enable!")
                    radarcham_status = True
                    time.sleep(3)
        
        
        if glow_status:
            glow()
        elif aimbot_status:
            if mouse.is_pressed("left"):
                pyautogui.keyDown("ctrl")
                if keyboard.is_pressed("alt"):
                    pyautogui.keyUp("ctrl")
                else:
                    print("left")
                    imbot()
                    pyautogui.keyUp("ctrl")
        elif radarcham_status:
            radarcham()
        elif noflash_status:
            noflash()
        
        
print(colorama.Fore.RESET)
