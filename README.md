PyOptris
================================
Python bindings for the Optris PI thermal imaging cameras.

# How to Use
Ensure that the SDK is extracted to `C:\lib\irDirectSDK`. Then to build run

```
python setup.pt build_ext --inplace
```

Then to use the library

```python
import pyoptris
pyoptris.usb_init('generic.xml')
pyoptris.set_palette(1)
pyoptris.set_palette_scale(1)
width, height = pyoptris.get_thermal_image_size() # (int, int)
thermalImage = pyoptris.get_thermal_image() # ndarray
paletteImage = pyoptris.get_palette_image() # ndarray
```

# Notes
This has been tested on Windows 10 with Miniconda 4.7.11, Python 3.7.4 64bit, Build Tools for Visual Studio 2019, and with an Optris PI 450 camera.

I am very new to working with the Python C API so there are likely lots of issues with the code, I was only coding with this for a short time to test a camera from a supplier. I am also new to writing Python extensions, especially using distutils, so this may also be incomplete.

I welcome any suggestions, pull requests, discussion, etc.

# Links

* [Optris PI 450](https://www.optris.global/thermal-imager-optris-pi400-pi450)

* [Optris PI SDK](https://www.optris.com/optris-pi-sdk)

* [libirimager API](http://documentation.evocortex.com/libirimager2/html/index.html)

* [Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017)

