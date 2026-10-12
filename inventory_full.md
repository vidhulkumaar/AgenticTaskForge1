| File | Function | Line | Duration | Purpose | Category | Replace? | Observable Condition | Recommended Mechanism | Risk |
|---|---|---:|---:|---|---|---|---|---|---|
| agent_orchestrator.py | agent_loop() | 426 | STEP_DELAY | Agent step pacing | Category I | MAY REMAIN | N/A | N/A | None |
| agent_orchestrator.py | agent_loop() | 482 | STEP_DELAY | Agent step pacing | Category I | MAY REMAIN | N/A | N/A | None |
| classify_sleeps.py | classify_sleep() | 4 | path, func, duration, context | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| classify_sleeps.py | classify_sleep() | 48 | path, func, dur, ctx | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task2_1_browser_navigation.py | open_in_active_system_chrome() | 61 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task2_2_form_interaction.py | execute_action_step() | 202 | 0.3 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| task2_2_form_interaction.py | execute_action_step() | 263 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task2_2_form_interaction.py | execute_action_step() | 265 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task2_2_form_interaction.py | run_task_2_2() | 341 | 2 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| task2_2_form_interaction.py | run_task_2_2() | 352 | 1 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task2_4_desktop_interaction.py | connect_to_app() | 110 | 2 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task2_4_desktop_interaction.py | action_click() | 180 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task2_4_desktop_interaction.py | action_type_text() | 199 | 0.1 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task2_4_desktop_interaction.py | action_type_text() | 201 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task2_4_desktop_interaction.py | action_type_text() | 206 | 0.2 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task2_4_desktop_interaction.py | action_type_text() | 209 | 0.1 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task2_4_desktop_interaction.py | action_type_text() | 213 | 0.3 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task2_4_desktop_interaction.py | action_focus_window() | 251 | 0.3 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task2_4_desktop_interaction.py | run_task_2_4() | 300 | 0.3 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task2_5_nl_pipeline.py | execute_browser_navigate() | 195 | 1.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task2_5_nl_pipeline.py | execute_browser_navigate() | 202 | 1.5 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| task2_5_nl_pipeline.py | run_pipeline() | 369 | 0.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_1_calculator.py | launch_calculator() | 199 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task3_1_calculator.py | launch_calculator() | 209 | 0.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_1_calculator.py | click_button() | 253 | 0.05 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | press_clear() | 312 | 0.15 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task3_1_calculator.py | press_clear() | 315 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | press_clear() | 317 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | press_clear() | 319 | 0.15 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_expression_via_keyboard() | 329 | 0.2 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task3_1_calculator.py | enter_expression_via_keyboard() | 334 | 0.05 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_expression_via_keyboard() | 337 | 0.05 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_expression_via_keyboard() | 340 | 0.08 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_expression_via_keyboard() | 344 | 0.35 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_unary_via_keyboard() | 353 | 0.2 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_unary_via_keyboard() | 357 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_unary_via_keyboard() | 363 | 0.2 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | enter_unary_via_keyboard() | 385 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | execute_expression_in_calc() | 394 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | execute_expression_in_calc() | 401 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task3_1_calculator.py | run_task_3_1() | 447 | 0.5 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task3_2_system_settings.py | set_wifi() | 124 | 1.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_brightness() | 169 | 0.4 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_brightness() | 181 | 0.4 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_volume() | 223 | 0.15 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_mute() | 233 | 0.1 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_bluetooth() | 282 | 1.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_theme_mode() | 321 | 0.3 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_power_plan() | 388 | 0.3 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task3_2_system_settings.py | set_firewall() | 419 | 0.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task5_privacy_dashboard.py | start() | 225 | 1.2 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task5_privacy_dashboard.py | _demo_agent() | 727 | 1.0 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task6_computer_control.py | _enum() | 199 | 0.6 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task6_computer_control.py | _enum() | 219 | 3.5 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task6_computer_control.py | _enum() | 225 | 3 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task6_computer_control.py | press_key() | 247 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_computer_control.py | type_anywhere() | 261 | 0.2 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_computer_control.py | type_anywhere() | 263 | 0.4 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_computer_control.py | click_text() | 346 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_computer_control.py | clear_input() | 358 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_computer_control.py | clear_input() | 360 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | _focus_window() | 57 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task6_electron_apps.py | _focus_window() | 60 | 1 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task6_electron_apps.py | _type_and_send() | 68 | 0.3 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | _type_and_send() | 71 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | _launch_whatsapp() | 105 | 4 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task6_electron_apps.py | whatsapp_send_message() | 122 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 124 | 0.8 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 129 | 1.5 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 133 | 1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 142 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 147 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | whatsapp_send_message() | 150 | 0.5 | Unknown delay | Other | PARTIAL | Unknown | Requires manual inspection | Medium |
| task6_electron_apps.py | whatsapp_read_last() | 170 | 0.8 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | whatsapp_read_last() | 173 | 1.5 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | whatsapp_read_last() | 175 | 1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | _launch_spotify() | 231 | 5 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task6_electron_apps.py | spotify_play_pause() | 241 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_next() | 252 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_prev() | 262 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_search() | 274 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task6_electron_apps.py | spotify_search() | 278 | 0.8 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_search() | 282 | 0.2 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | spotify_search() | 285 | 1.5 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | spotify_search() | 287 | 2 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_search() | 291 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_search() | 293 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | spotify_get_current() | 306 | 0.5 | Wait for screen to settle before OCR | Category F | PARTIAL | UI state reached | Wait for specific UI element before OCR | High |
| task6_electron_apps.py | spotify_volume() | 320 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | _launch_discord() | 376 | 6 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| task6_electron_apps.py | discord_navigate_channel() | 391 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task6_electron_apps.py | discord_navigate_channel() | 395 | 0.8 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | discord_navigate_channel() | 399 | 0.2 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | discord_navigate_channel() | 402 | 1 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | discord_navigate_channel() | 406 | 1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | discord_send_message() | 426 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task6_electron_apps.py | discord_send_message() | 437 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | discord_send_message() | 443 | 0.3 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| task6_electron_apps.py | discord_send_message() | 446 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| task6_electron_apps.py | discord_read_channel() | 455 | 1 | Wait for screen to settle before OCR | Category F | PARTIAL | UI state reached | Wait for specific UI element before OCR | High |
| execution\browser.py | action_browser_go_back() | 100 | 1 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| execution\browser.py | action_browser_go_forward() | 108 | 1 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| execution\browser.py | action_fill_form() | 137 | 0.4 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\browser.py | action_fill_form() | 140 | 1.5 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| execution\browser.py | action_fill_form() | 148 | 0.3 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| execution\browser.py | action_fill_form() | 152 | 1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\browser.py | action_click_browser_element() | 168 | 0.8 | Wait for page navigation | Category E | YES | DOM loaded or element visible | Playwright wait_for_selector / wait_for_url | Low |
| execution\desktop.py | action_open_app() | 10 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| execution\desktop.py | action_open_app() | 14 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
| execution\desktop.py | action_open_app() | 25 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| execution\desktop.py | action_type_text() | 36 | 0.3 | Wait for clipboard to sync | Category G | YES | Clipboard contains value | Bounded loop checking pyperclip.paste() | Medium |
| execution\desktop.py | action_type_text() | 38 | 0.1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\desktop.py | action_type_text() | 40 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\desktop.py | action_save_file() | 63 | 1.5 | Wait for file operation | Category D | YES | Path.exists() == True | Bounded while loop poll | Low |
| execution\desktop.py | action_save_file() | 69 | 0.3 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\desktop.py | action_save_file() | 71 | 1 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\desktop.py | action_save_file() | 77 | 0.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait(ready) | Medium |
| execution\desktop.py | action_save_file() | 83 | 0.5 | Wait for file operation | Category D | YES | Path.exists() == True | Bounded while loop poll | Low |
| execution\filesystem.py | action_open_folder() | 20 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait(ready) / EnumWindows | Low |
