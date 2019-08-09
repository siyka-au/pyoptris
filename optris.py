from ctypes import CDLL, c_int, c_float, byref

lib = CDLL('.\\libirimager.dll')

def usb_init(xml_config: str, formats_def: str = None, log_file: str = None) -> int:
    return lib.evo_irimager_usb_init(xml_config.encode(), None if formats_def is None else formats_def.encode(), None if log_file is None else log_file.encode())

def tcp_init(ip: str, port: int) -> int:
    return lib.evo_irimager_tcp_init(ip.encode(), port)

def terminate() -> int:
    return lib.evo_irimager_terminate(None)

def get_thermal_image_size() -> (int, int):
    width = c_int()
    height = c_int()
    _ = lib.evo_irimager_get_thermal_image_size(byref(width), byref(height))
    return width.value, height.value

def get_palette_image_size() -> (int, int):
    width = c_int()
    height = c_int()
    _ = lib.evo_irimager_get_palette_image_size(byref(width), byref(height))
    return width.value, height.value

# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image(int* w, int* h, unsigned short* data);

# __IRDIRECTSDK_API__ int evo_irimager_get_palette_image(int* w, int* h, unsigned char* data);

# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_palette_image(int w_t, int h_t, unsigned short* data_t, int w_p, int h_p, unsigned char* data_p );

def set_palette(id: int) -> int:
    return lib.evo_irimager_set_palette(id)

def set_palette_scale(scale: int) -> int:
    return lib.evo_irimager_set_palette_scale(scale)

def set_shutter_mode(mode: int) -> int:
    return lib.evo_irimager_set_shutter_mode(mode)

def trigger_shutter_flag() -> int:
    return lib.evo_irimager_trigger_shutter_flag(None)

def set_temperature_range(min: int, max: int) -> int:
    return lib.evo_irimager_set_temperature_range(min, max)

def set_radiation_parameters(emissivity: float, transmissivity: float, ambientTemperature: float) -> int:
    return lib.evo_irimager_set_radiation_parameters(emissivity, transmissivity, ambientTemperature)

# __IRDIRECTSDK_API__ int evo_irimager_to_palette_save_png(unsigned short* thermal_data, int w, int h, const char* path, int palette, int palette_scale);

def set_focusmotor_pos(position: float) -> int:
    return lib.evo_irimager_set_focusmotor_pos(position)

def get_focusmotor_pos() -> float:
    position = c_float()
    _ = lib.evo_irimager_get_focusmotor_pos(byref(position))
    return position.value

def daemon_launch() -> int:
    return lib.evo_irimager_daemon_launch(None)

def daemon_is_running() -> int:
    return lib.evo_irimager_daemon_is_running(None)

def daemon_kill() -> int:
    return lib.evo_irimager_daemon_kill(None)

usb_init('.\\generic.xml')
w, h = get_thermal_image_size()
print('{} x {}'.format(w, h))

terminate()