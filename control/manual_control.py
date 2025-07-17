def run_manual(master):
    import __main__

    js = init_joystick()
    if js is None:
        print("[INFO] Manual control could not be started.")
        return

    is_armed, mode = check_arm_status(master)
    print(f"[INFO] Flight Mode: {mode}")
    print(f"[INFO] ARM Status: {'ARMED' if is_armed else 'DISARMED'}")

    # Arming required before MANUAL_CONTROL
    if not is_armed:
        print("[INFO] Arming vehicle...")
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
        master.motors_armed_wait()
        print("[✓] Vehicle armed.")

    print("[INFO] Manual control started. Press Ctrl+C to stop.")
    try:
        while True:
            pygame.event.pump()

            thrust_joystick = -js.get_axis(1)   # Forward/back (joystick Y ekseni)
            steer_joystick = js.get_axis(0)    # Yaw (joystick X ekseni)

            # MAVLink MANUAL_CONTROL x, y, r değerleri için -1000 ile 1000 arası
            x = int(constrain(thrust_joystick, -1, 1) * 1000)   # İleri/Geri kontrolü
            y = 0                                      # Yanal hareket (kullanılmıyor)

            # Gaz (Throttle) kontrolü: Joystick'in -1 ile 1 aralığını MAVLink'in 0 (minimum) ile 1000 (maksimum) aralığına ölçekle
            # -1 -> 0 (min gaz)
            #  0 -> 500 (orta gaz)
            #  1 -> 1000 (max gaz)
            z = int(constrain(thrust_joystick, -1, 1) * 500 + 500)

            # Yaw kontrolü: -1000 ile 1000 arası
            r = int(constrain(steer_joystick, -1, 1) * 1000)
            buttons = 0

            master.mav.manual_control_send(
                config.TARGET_SYSTEM,
                x, y, z, r, buttons
            )

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[INFO] Manual control stopped.")
        print("[INFO] Disarming vehicle...")

        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        master.motors_disarmed_wait()
        print("[✓] Vehicle disarmed.")

        print("[INFO] Returning to main menu...")
        os.execv(__main__.__file__, ['python3'] + [__main__.__file__])
