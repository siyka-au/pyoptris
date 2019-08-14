from setuptools import setup, Extension
import platform
from numpy.distutils.misc_util import get_numpy_include_dirs

if platform.system() == 'Windows':
    optrisInclude = "C:\\lib\\irDirectSDK\\sdk"
    if  platform.architecture()[0] == '64bit':
        optrisLib = "C:\\lib\\irDirectSDK\\sdk\\x64"
    else:
        optrisLib = "C:\\lib\\irDirectSDK\\sdk\\Win32"
else:
    optrisInclude = "/usr/local/include"
    optrisLib = "/usr/local/lib"

pyoptris = Extension( "pyoptris",
    [ "_pyoptris.cpp" ],
    include_dirs=get_numpy_include_dirs() + [ ".", optrisInclude ],
    library_dirs=[ optrisLib ],
    libraries=[ 'libirimager' ],
    language='c++',
)

setup(
    name='PyOptris',
    version='1.0',
    description='Python bindings for Optris SDK',
    author_email='mikey@mookins.com',
    url='https://github.com/siyka-au/pyoptris',
    ext_modules=[ pyoptris ],
)
