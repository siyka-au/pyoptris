import ctypes
import numpy
import matplotlib.pyplot as plt

lib = ctypes.CDLL('.\\libirimager.dll')

def usb_init(xml_config: str, formats_def: str = None, log_file: str = None) -> int:
    return lib.evo_irimager_usb_init(xml_config.encode(), None if formats_def is None else formats_def.encode(), None if log_file is None else log_file.encode())

def tcp_init(ip: str, port: int) -> int:
    return lib.evo_irimager_tcp_init(ip.encode(), port)

def terminate() -> int:
    return lib.evo_irimager_terminate(None)

def get_thermal_image_size() -> (int, int):
    width = ctypes.c_int()
    height = ctypes.c_int()
    _ = lib.evo_irimager_get_thermal_image_size(ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value

def get_palette_image_size() -> (int, int):
    width = ctypes.c_int()
    height = ctypes.c_int()
    _ = lib.evo_irimager_get_palette_image_size(ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value

# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image(int* w, int* h, unsigned short* data);
def get_thermal_image(width: int, height: int) -> numpy.ndarray:
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    thermalData = numpy.empty((height, width), dtype=numpy.uint16)
    thermalDataPointer = thermalData.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
    _ = lib.evo_irimager_get_thermal_image(w, h, thermalDataPointer)
    return thermalData

# __IRDIRECTSDK_API__ int evo_irimager_get_palette_image(int* w, int* h, unsigned char* data);
def get_palette_image(width: int, height: int) -> numpy.ndarray:
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    paletteData = numpy.empty((height, width, 3), dtype=numpy.uint8)
    paletteDataPointer = paletteData.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    retVal = -1
    while retVal != 0:
        retVal = lib.evo_irimager_get_palette_image(w, h, paletteDataPointer)
    return paletteData

# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_palette_image(int w_t, int h_t, unsigned short* data_t, int w_p, int h_p, unsigned char* data_p );
def get_thermal_palette_image(width: int, height: int) -> (numpy.ndarray, numpy.ndarray):
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    thermalData = numpy.empty((height, width), dtype=numpy.uint16)
    paletteData = numpy.empty((height, width, 3), dtype=numpy.uint8)
    thermalDataPointer = thermalData.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
    paletteDataPointer = paletteData.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    _ = lib.evo_irimager_get_palette_image(w, h, thermalDataPointer, w, h, paletteDataPointer)
    return (thermalData, paletteData)

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

def set_focus_motor_position(position: float) -> int:
    return lib.evo_irimager_set_focusmotor_pos(position)

def get_focus_motor_position() -> float:
    position = ctypes.c_float()
    _ = lib.evo_irimager_get_focusmotor_pos(ctypes.byref(position))
    return position.value

def daemon_launch() -> int:
    return lib.evo_irimager_daemon_launch(None)

def daemon_is_running() -> int:
    return lib.evo_irimager_daemon_is_running(None)

def daemon_kill() -> int:
    return lib.evo_irimager_daemon_kill(None)

if __name__ == "__main__":
    usb_init('.\\generic.xml')

    set_palette(1)
    w, h = get_thermal_image_size()
    print('{} x {}'.format(w, h))

    frame = get_palette_image(w, h)
    plt.imshow(frame)
    plt.show()

    terminate()