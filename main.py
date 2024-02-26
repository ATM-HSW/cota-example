import ota
import wifi
import time
from your_module import your_custom_function


def conn_wifi(ssid: str, password: str, max_retries: int = 3, retry_delay: int = 5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"Connecting to: {ssid}")
            wifi.radio.connect(ssid, password)
            print(f"Connected to: {ssid}")
            return
        except ConnectionError as e:
            retry_count += 1
            print(f"Connection attempt {retry_count} failed: {e}")
            if retry_count < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    print("Max retries reached. Unable to establish connection.")


def main():    
    settings = ota.get_thingsboard_settings()
    conn_wifi(settings["wifi_ssid"], settings["wifi_password"])
    tb_ota = ota.OverTheAirUpdate(tb_url=settings["thingsboard_url"], 
                                  tb_port=settings["thingsboard_port"], 
                                  tb_device_access_token=settings["thingsboard_device_token"])

    while True:
        try:
            if tb_ota.is_new_firmware_available():
                # New firmware is available, let's download it.
                tb_ota.download_firmware_files()
            else:
                # Add your custom code here.
                your_custom_function()
        except ConnectionError as e:
            # Handle request connection errors here, e.g. you might try to reconnect to Wi-Fi (Optional).
            conn_wifi()   
        except ota.OverTheAirUpdateError as e:
            # Handle exceptions related to the firmware download process (Optional).
            print(e)   


if __name__ == '__main__':
    main()
