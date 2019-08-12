#include <Python.h>
#include <direct_binding.h>

/**
 * @brief Initializes an IRImager instance connected to this computer via USB
 * @param[in] xml_config path to xml config
 * @param[in] formats_def path to Formats.def file. Set zero for standard value.
 * @param[in] log_file path to log file. Set zero for standard value.
 * @return 0 on success, -1 on error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_usb_init(const char* xml_config, const char* formats_def, const char* log_file);
 * 
 */
PyObject* usb_init(PyObject *, PyObject *args) {
    const char* xml_config;
    const char* formats_def;
    const char* log_file;
    if (!PyArg_ParseTuple(args, "s|zz", &xml_config, &formats_def, &log_file)) {
        PyErr_SetString(PyExc_RuntimeError, "Bad argument(s)");
        return NULL;
    }
    int ok = evo_irimager_usb_init(xml_config, formats_def, log_file);
    switch(ok) {
        case 0:
            Py_RETURN_NONE;
        
        case -1:
            PyErr_SetString(PyExc_RuntimeError, "Error");
            break;

        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown error");
    }
    return NULL;
}

/**
 * @brief Initializes the TCP connection to the daemon process (non-blocking)
 * @param[in] IP address of the machine where the daemon process is running ("localhost" can be resolved)
 * @param port Port of daemon, default 1337
 * @return  error code: 0 on success, -1 on host not found (wrong IP, daemon not running), -2 on fatal error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_tcp_init(const char* ip, int port);
 * 
 */
PyObject* tcp_init(PyObject *, PyObject *args) {
    const char* ip;
    int port;
    if (!PyArg_ParseTuple(args, "si", &ip, &port)) {
        PyErr_SetString(PyExc_RuntimeError, "Bad argument(s)");
        return NULL;
    }
    int ok = evo_irimager_tcp_init(ip, port);
    switch(ok) {
        case 0:
            Py_RETURN_NONE;
        
        case -1:
            PyErr_SetString(PyExc_RuntimeError, "Host not found");
            break;
        
        case -2:
            PyErr_SetString(PyExc_RuntimeError, "Fatal error");
            break;
        
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown error");
    }
    return NULL;
}

/**
 * @brief Disconnects the camera, either connected via USB or TCP
 * @return 0 on success, -1 on error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_terminate();
 * 
 */
PyObject* terminate(PyObject *, PyObject *) {
    int ok = evo_irimager_terminate();
    switch(ok) {
        case 0:
            Py_RETURN_NONE;
        
        case -1:
            PyErr_SetString(PyExc_RuntimeError, "Error");
            break;
        
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown error");
    }
    return NULL;
}

/**
 * @brief Accessor to image width and height
 * @param[out] w width
 * @param[out] h height
 * @return 0 on success, -1 on error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image_size(int* w, int* h);
 * 
 */
PyObject* get_thermal_image_size(PyObject *, PyObject *) {
    int width, height;
    int ok = evo_irimager_get_thermal_image_size(&width, &height);
    switch(ok) {
        case 0:
            return Py_BuildValue("ii", width, height);
        
        case -1:
            PyErr_SetString(PyExc_RuntimeError, "Error");
            break;
        
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown error");
    }
    return NULL;
}

/**
 * @brief Accessor to width and height of false color coded palette image
 * @param[out] w width
 * @param[out] h height
 * @return 0 on success, -1 on error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_palette_image_size(int* w, int* h);
 * 
 */
PyObject* get_palette_image_size(PyObject *, PyObject *) {
    int width, height;
    int ok = evo_irimager_get_palette_image_size(&width, &height);
    switch(ok) {
        case 0:
            return Py_BuildValue("ii", width, height);
        
        case -1:
            PyErr_SetString(PyExc_RuntimeError, "Error");
            break;
        
        default:
            PyErr_SetString(PyExc_RuntimeError, "Unknown error");
    }
    return NULL;
}

/**
 * @brief Accessor to thermal image by reference
 * Conversion to temperature values are to be performed as follows:
 * t = ((double)data[x] - 1000.0) / 10.0;
 * @param[in] w image width
 * @param[in] h image height
 * @param[out] data pointer to unsigned short array allocate by the user (size of w * h)
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_thermal_image(int* w, int* h, unsigned short* data);
 * 
 */
PyObject* get_thermal_image(PyObject *, PyObject *args) {
    double x = PyFloat_AsDouble(args);
    double result = 6;
    return PyFloat_FromDouble(result);
}

/**
 * @brief Accessor to an RGB palette image by reference
 * data format: unsigned char array (size 3 * w * h) r,g,b
 * @param[in] w image width
 * @param[in] h image height
 * @param[out] data pointer to unsigned char array allocate by the user (size of 3 * w * h)
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_palette_image(int* w, int* h, unsigned char* data);
 * 
 */
PyObject* get_palette_image(PyObject *, PyObject *args) {
    double x = PyFloat_AsDouble(args);
    double result = 7;
    return PyFloat_FromDouble(result);
}

/**
 * @brief Accessor to an RGB palette image and a thermal image by reference
 * @param[in] w_t width of thermal image
 * @param[in] h_t height of thermal image
 * @param[out] data_t data pointer to unsigned short array allocate by the user (size of w * h)
 * @param[in] w_p width of palette image (can differ from thermal image width due to striding)
 * @param[in] h_p height of palette image (can differ from thermal image height due to striding)
 * @param[out] data_p data pointer to unsigned char array allocate by the user (size of 3 * w * h)
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_thermal_palette_image(int w_t, int h_t, unsigned short* data_t, int w_p, int h_p, unsigned char* data_p );
 * 
 */

/**
 * @brief sets palette format to daemon.
 * Defined in IRImager Direct-SDK, see
 * enum EnumOptrisColoringPalette{eAlarmBlue   = 1,
 *                                eAlarmBlueHi = 2,
 *                                eGrayBW      = 3,
 *                                eGrayWB      = 4,
 *                                eAlarmGreen  = 5,
 *                                eIron        = 6,
 *                                eIronHi      = 7,
 *                                eMedical     = 8,
 *                                eRainbow     = 9,
 *                                eRainbowHi   = 10,
 *                                eAlarmRed    = 11 };
 *
 * @param id palette id
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_palette(int id);
 * 
 */
PyObject* set_palette(PyObject *, PyObject* args) {
    double x = PyFloat_AsDouble(o);
    double result = 7;
    return PyFloat_FromDouble(result);
}

/**
 * @brief sets palette scaling method
 * Defined in IRImager Direct-SDK, see
 * enum EnumOptrisPaletteScalingMethod{eManual = 1,
 *                                     eMinMax = 2,
 *                                     eSigma1 = 3,
 *                                     eSigma3 = 4 };
 * @param scale scaling method id
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_palette_scale(int scale);
 * 
 */
PyObject* set_palette_scale(PyObject *, PyObject* args) {
    double x = PyFloat_AsDouble(o);
    double result = 7;
    return PyFloat_FromDouble(result);
}

/**
 * @brief sets shutter flag control mode
 * @param mode 0 means manual control, 1 means automode
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_shutter_mode(int mode);
 * 
 */

/**
 * @brief forces a shutter flag cycle
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_trigger_shutter_flag();
 * 
 */

/**
 * @brief sets the minimum and maximum remperature range to the camera (also configurable in xml-config)
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_temperature_range(int t_min, int t_max);
 * 
 */

/**
 * @brief sets radiation properties, i.e. emissivity and transmissivity parameters (not implemented for TCP connection, usb mode only)
 * @param[in] emissivity emissivity of observed object [0;1]
 * @param[in] transmissivity transmissivity of observed object [0;1]
 * @param[in] tAmbient ambient temperature, setting invalid values (below -273,15 degrees) forces the library to take its own measurement values.
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_radiation_parameters(float emissivity, float transmissivity, float tAmbient);
 * 
 */

/**
 * @brief 
 * @return error code: 0 on success, -1 on error
 *
 * __IRDIRECTSDK_API__ int evo_irimager_to_palette_save_png(unsigned short* thermal_data, int w, int h, const char* path, int palette, int palette_scale);
 *
 */

/**
 * @brief Set the position of the focusmotor
 * @param[in] pos fucos motor position in %
 * @return error code: 0 on success, -1 on error or if no focusmotor is available
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_set_focusmotor_pos(float pos);
 * 
 */

/**
 * @brief Get the position of the focusmotor
 * @param[out] posOut Data pointer to float for current fucos motor position in % (< 0 if no focusmotor available)
 * @return error code: 0 on success, -1 on error
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_get_focusmotor_pos(float *posOut);
 * 
 */

/**
 * Launch TCP daemon
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_daemon_launch();
 * 
 */

/**
 * Check whether daemon is already running
 * @return error code: 0 daemon is already active, -1 daemon is not started yet
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_daemon_is_running();
 * 
 */

/**
 * Kill TCP daemon
 * @return error code: 0 on success, -1 on error, -2 on fatal error (only TCP connection)
 * 
 * __IRDIRECTSDK_API__ int evo_irimager_daemon_kill();
 * 
 */

static PyMethodDef pyoptris_methods[] = {
    // The first property is the name exposed to Python, fast_tanh, the second is the C++
    // function name that contains the implementation.
    { "usb_init",               (PyCFunction) usb_init,               METH_VARARGS, nullptr },
    { "tcp_init",               (PyCFunction) tcp_init,               METH_VARARGS, nullptr },
    { "terminate",              (PyCFunction) terminate,              METH_NOARGS, nullptr },
    { "get_thermal_image_size", (PyCFunction) get_thermal_image_size, METH_NOARGS, nullptr },
    { "get_palette_image_size", (PyCFunction) get_palette_image_size, METH_NOARGS, nullptr },
    { "get_thermal_image",      (PyCFunction) get_thermal_image,      METH_NOARGS, nullptr },
    { "get_palette_image",      (PyCFunction) get_palette_image,      METH_NOARGS, nullptr },
    { "set_palette",            (PyCFunction) set_palette,            METH_O, nullptr },
    { "get_palette_image",      (PyCFunction) get_palette_image,      METH_NOARGS, nullptr },

    
    // Terminate the array with an object containing nulls.
    { nullptr, nullptr, 0, nullptr }
};

void _pyoptris_free(void *p) {
    evo_irimager_terminate();
}

// https://docs.python.org/3.4/c-api/module.html
static PyModuleDef pyoptris_module = {
    PyModuleDef_HEAD_INIT,
    "pyoptris",
    "Provides some functions, but faster",
    0,
    pyoptris_methods,
    NULL,
    NULL,
    NULL,
    _pyoptris_free
};

PyMODINIT_FUNC PyInit_pyoptris() {
    return PyModule_Create(&pyoptris_module);
}
