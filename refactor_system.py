import os
import re

with open('task3_2_system_settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Wifi
content = re.sub(
    r'        if result\.returncode == 0:\n            time\.sleep\(1\.5\)\n            return \{"success": True, "action": action, "interface": interface,\n                    "new_state": get_wifi_state\(interface\)\}',
    r'        if result.returncode == 0:\n            target_state = "enabled" if enable else "disabled"\n            end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n            while time.time() < end_t:\n                if get_wifi_state(interface) == target_state:\n                    break\n                time.sleep(0.2)\n            return {"success": True, "action": action, "interface": interface,\n                    "new_state": get_wifi_state(interface)}',
    content
)

# 2. Brightness
content = re.sub(
    r'                methods\[0\]\.WmiSetBrightness\(level, 0\)\n                time\.sleep\(0\.4\)\n                return \{"success": True, "target": level, "actual": get_brightness\(\)\}',
    r'                methods[0].WmiSetBrightness(level, 0)\n                end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n                while time.time() < end_t:\n                    if abs((get_brightness() or 0) - level) <= 5:\n                        break\n                    time.sleep(0.2)\n                return {"success": True, "target": level, "actual": get_brightness()}',
    content
)

content = re.sub(
    r'        if result\.returncode == 0:\n            time\.sleep\(0\.4\)\n            return \{"success": True, "target": level, "actual": get_brightness\(\)\}',
    r'        if result.returncode == 0:\n            end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n            while time.time() < end_t:\n                if abs((get_brightness() or 0) - level) <= 5:\n                    break\n                time.sleep(0.2)\n            return {"success": True, "target": level, "actual": get_brightness()}',
    content
)

# 3. Volume
content = re.sub(
    r'        ep\.SetMasterVolumeLevelScalar\(level / 100\.0, None\)\n        time\.sleep\(0\.15\)\n        return \{"success": True, "target": level, "actual": get_volume\(\)\}',
    r'        ep.SetMasterVolumeLevelScalar(level / 100.0, None)\n        end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n        while time.time() < end_t:\n            if abs((get_volume() or 0) - level) <= 2:\n                break\n            time.sleep(0.1)\n        return {"success": True, "target": level, "actual": get_volume()}',
    content
)

content = re.sub(
    r'        ep\.SetMute\(1 if mute else 0, None\)\n        time\.sleep\(0\.1\)\n        return \{"success": True, "muted": get_mute_state\(\)\}',
    r'        ep.SetMute(1 if mute else 0, None)\n        end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n        while time.time() < end_t:\n            if get_mute_state() == mute:\n                break\n            time.sleep(0.1)\n        return {"success": True, "muted": get_mute_state()}',
    content
)

# 4. Bluetooth
content = re.sub(
    r'        result = subprocess\.run\(\n            \["powershell", "-NoProfile", "-Command", cmd\],\n            capture_output=True, text=True\n        \)\n        time\.sleep\(1\.5\)\n        new_state = get_bluetooth_state\(\)',
    r'        result = subprocess.run(\n            ["powershell", "-NoProfile", "-Command", cmd],\n            capture_output=True, text=True\n        )\n        target_state = "enabled" if enable else "disabled"\n        end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n        while time.time() < end_t:\n            new_state = get_bluetooth_state()\n            if new_state == target_state:\n                break\n            time.sleep(0.5)\n        new_state = get_bluetooth_state()',
    content
)

# 5. Theme
content = re.sub(
    r'            "ImmersiveColorSet", 2, 5000, None\n        \)\n        time\.sleep\(0\.3\)\n        actual = get_theme_mode\(\)',
    r'            "ImmersiveColorSet", 2, 5000, None\n        )\n        target = "dark" if dark else "light"\n        end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n        while time.time() < end_t:\n            actual = get_theme_mode()\n            if actual == target:\n                break\n            time.sleep(0.2)\n        actual = get_theme_mode()',
    content
)

# 6. Power Plan
content = re.sub(
    r'    result = subprocess\.run\(\n        \["powercfg", "/setactive", best\["guid"\]\], capture_output=True\n    \)\n    time\.sleep\(0\.3\)\n    active = get_active_power_plan\(\)',
    r'    result = subprocess.run(\n        ["powercfg", "/setactive", best["guid"]], capture_output=True\n    )\n    end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n    while time.time() < end_t:\n        active = get_active_power_plan()\n        if active and best["name"].lower() in active.lower():\n            break\n        time.sleep(0.2)\n    active = get_active_power_plan()',
    content
)

# 7. Firewall
content = re.sub(
    r'        if result\.returncode == 0:\n            time\.sleep\(0\.5\)\n            return \{"success": True, "new_state": get_firewall_state\(\)\}',
    r'        if result.returncode == 0:\n            target = "enabled" if enable else "disabled"\n            end_t = time.time() + Config.UI_ELEMENT_TIMEOUT\n            while time.time() < end_t:\n                if get_firewall_state() == target:\n                    break\n                time.sleep(0.2)\n            return {"success": True, "new_state": get_firewall_state()}',
    content
)

with open('task3_2_system_settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

