from enum import Enum
import ctypes
import numpy
import matplotlib.pyplot as plt

lib = ctypes.CDLL('.\\libirimager.dll')

#
# @brief Initializes an IRImager instance connected to this computer via USB
# @param[in] xml_config path to xml config
# @param[in] formats_def path to Formats.def file. Set zero for standard value.
# @param[in] log_file path to log file. Set zero for standard value.
# @return 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_usb_init(const char* xml_config, const char* formats_def, const char* log_file);
#
def usb_init(xml_config: str, formats_def: str = None, log_file: str = None) -> int:
    return lib.evo_irimager_usb_init(xml_config.encode(), None if formats_def is None else formats_def.encode(), None if log_file is None else log_file.encode())

#
# @brief Initializes the TCP connection to the daemon process (non-blocking)
# @param[in] IP address of the machine where the daemon process is running ("localhost" can be resolved)
# @param port Port of daemon, default 1337
# @return  error code: 0 on success, -1 on host not found (wrong IP, daemon not running), -2 on fatal error
#
# __IRDIRECTSDK_API__ int evo_irimager_tcp_init(const char* ip, int port);
#
def tcp_init(ip: str, port: int) -> int:
    return lib.evo_irimager_tcp_init(ip.encode(), port)

#
# @brief Disconnects the camera, either connected via USB or TCP
# @return 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_terminate();
#
def terminate() -> int:
    return lib.evo_irimager_terminate(None)

#
# @brief Accessor to image width and height
# @param[out] w width
# @param[out] h height
# @return 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image_size(int* w, int* h);
#
def get_thermal_image_size() -> (int, int):
    width = ctypes.c_int()
    height = ctypes.c_int()
    _ = lib.evo_irimager_get_thermal_image_size(ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value

#
# @brief Accessor to width and height of false color coded palette image
# @param[out] w width
# @param[out] h height
# @return 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_get_palette_image_size(int* w, int* h);
#
def get_palette_image_size() -> (int, int):
    width = ctypes.c_int()
    height = ctypes.c_int()
    _ = lib.evo_irimager_get_palette_image_size(ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value

#
# @brief Accessor to thermal image by reference
# Conversion to temperature values are to be performed as follows:
# t = ((double)data[x] - 1000.0) / 10.0;
# @param[in] w image width
# @param[in] h image height
# @param[out] data pointer to unsigned short array allocate by the user (size of w * h)
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image(int* w, int* h, unsigned short* data);
#
def get_thermal_image(width: int, height: int) -> numpy.ndarray:
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    thermalData = numpy.empty((height, width), dtype=numpy.uint16)
    thermalDataPointer = thermalData.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
    _ = lib.evo_irimager_get_thermal_image(w, h, thermalDataPointer)
    return thermalData

#
# @brief Accessor to an RGB palette image by reference
# data format: unsigned char array (size 3 * w * h) r,g,b
# @param[in] w image width
# @param[in] h image height
# @param[out] data pointer to unsigned char array allocate by the user (size of 3 * w * h)
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_get_palette_image(int* w, int* h, unsigned char* data);
#
def get_palette_image(width: int, height: int) -> numpy.ndarray:
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    paletteData = numpy.empty((height, width, 3), dtype=numpy.uint8)
    paletteDataPointer = paletteData.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    retVal = -1
    while retVal != 0:
        retVal = lib.evo_irimager_get_palette_image(w, h, paletteDataPointer)
    return paletteData

#
# @brief Accessor to an RGB palette image and a thermal image by reference
# @param[in] w_t width of thermal image
# @param[in] h_t height of thermal image
# @param[out] data_t data pointer to unsigned short array allocate by the user (size of w * h)
# @param[in] w_p width of palette image (can differ from thermal image width due to striding)
# @param[in] h_p height of palette image (can differ from thermal image height due to striding)
# @param[out] data_p data pointer to unsigned char array allocate by the user (size of 3 * w * h)
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
#__IRDIRECTSDK_API__ int evo_irimager_get_thermal_palette_image(int w_t, int h_t, unsigned short* data_t, int w_p, int h_p, unsigned char* data_p );
#
def get_thermal_palette_image(width: int, height: int) -> (numpy.ndarray, numpy.ndarray):
    w = ctypes.byref(ctypes.c_int(width))
    h = ctypes.byref(ctypes.c_int(height))
    thermalData = numpy.empty((height, width), dtype=numpy.uint16)
    paletteData = numpy.empty((height, width, 3), dtype=numpy.uint8)
    thermalDataPointer = thermalData.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
    paletteDataPointer = paletteData.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    _ = lib.evo_irimager_get_palette_image(w, h, thermalDataPointer, w, h, paletteDataPointer)
    return (thermalData, paletteData)

#
# @brief sets palette format to daemon.
# Defined in IRImager Direct-SDK, see
# enum EnumOptrisColoringPalette{eAlarmBlue   = 1,
#                                eAlarmBlueHi = 2,
#                                eGrayBW      = 3,
#                                eGrayWB      = 4,
#                                eAlarmGreen  = 5,
#                                eIron        = 6,
#                                eIronHi      = 7,
#                                eMedical     = 8,
#                                eRainbow     = 9,
#                                eRainbowHi   = 10,
#                                eAlarmRed    = 11 };
#
# @param id palette id
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_set_palette(int id);
#
class ColouringPalette(Enum):
    ALARM_BLUE = 1
    ALARM_BLUE_HI = 2
    GRAY_BW = 3
    GRAY_WB = 4
    ALARM_GREEN = 5
    IRON = 6
    IRON_HI = 7
    MEDICAL = 8
    RAINBOW = 9
    RAINBOW_HI = 10
    ALARM_RED = 11

def set_palette(colouringPalette: ColouringPalette) -> int:
    return lib.evo_irimager_set_palette(colouringPalette)

#
# @brief sets palette scaling method
# Defined in IRImager Direct-SDK, see
# enum EnumOptrisPaletteScalingMethod{eManual = 1,
#                                     eMinMax = 2,
#                                     eSigma1 = 3,
#                                     eSigma3 = 4 };
# @param scale scaling method id
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_set_palette_scale(int scale);
#
class PaletteScalingMethod(Enum):
    MANUAL = 1
    MIN_MAX = 2
    SIGMA1 = 3
    SIGMA3 = 4

def set_palette_scale(paletteScalingMethod: PaletteScalingMethod) -> int:
    return lib.evo_irimager_set_palette_scale(paletteScalingMethod)

#
# @brief sets shutter flag control mode
# @param mode 0 means manual control, 1 means automode
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_set_shutter_mode(int mode);
#
class ShutterMode(Enum):
    MANUAL = 0
    AUTO = 1

def set_shutter_mode(shutterMode: ShutterMode) -> int:
    return lib.evo_irimager_set_shutter_mode(shutterMode)

#
# @brief forces a shutter flag cycle
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_trigger_shutter_flag();
#
def trigger_shutter_flag() -> int:
    return lib.evo_irimager_trigger_shutter_flag(None)

#
# @brief sets the minimum and maximum remperature range to the camera (also configurable in xml-config)
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_set_temperature_range(int t_min, int t_max);
#
def set_temperature_range(min: int, max: int) -> int:
    return lib.evo_irimager_set_temperature_range(min, max)

#
# @brief sets radiation properties, i.e. emissivity and transmissivity parameters (not implemented for TCP connection, usb mode only)
# @param[in] emissivity emissivity of observed object [0;1]
# @param[in] transmissivity transmissivity of observed object [0;1]
# @param[in] tAmbient ambient temperature, setting invalid values (below -273,15 degrees) forces the library to take its own measurement values.
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_set_radiation_parameters(float emissivity, float transmissivity, float tAmbient);
#
def set_radiation_parameters(emissivity: float, transmissivity: float, ambientTemperature: float) -> int:
    return lib.evo_irimager_set_radiation_parameters(emissivity, transmissivity, ambientTemperature)

#
# @brief 
# @return error code: 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_to_palette_save_png(unsigned short* thermal_data, int w, int h, const char* path, int palette, int palette_scale);
#

#
# @brief Set the position of the focusmotor
# @param[in] pos fucos motor position in %
# @return error code: 0 on success, -1 on error or if no focusmotor is available
#
# __IRDIRECTSDK_API__ int evo_irimager_set_focusmotor_pos(float pos);
#
def set_focus_motor_position(position: float) -> int:
    return lib.evo_irimager_set_focusmotor_pos(position)

#
# @brief Get the position of the focusmotor
# @param[out] posOut Data pointer to float for current fucos motor position in % (< 0 if no focusmotor available)
# @return error code: 0 on success, -1 on error
#
# __IRDIRECTSDK_API__ int evo_irimager_get_focusmotor_pos(float *posOut);
#
def get_focus_motor_position() -> float:
    position = ctypes.c_float()
    _ = lib.evo_irimager_get_focusmotor_pos(ctypes.byref(position))
    return position.value

#
# Launch TCP daemon
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_daemon_launch();
#
def daemon_launch() -> int:
    return lib.evo_irimager_daemon_launch(None)

#
# Check whether daemon is already running
# @return error code: 0 daemon is already active, -1 daemon is not started yet
#
# __IRDIRECTSDK_API__ int evo_irimager_daemon_is_running();
#
def daemon_is_running() -> int:
    return lib.evo_irimager_daemon_is_running(None)

#
# Kill TCP daemon
# @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
#
# __IRDIRECTSDK_API__ int evo_irimager_daemon_kill();
#
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