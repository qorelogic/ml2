
# python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
	Extension("calcpi",
		["calcpi.pyx"],		
	)
]

setup(
	name = "Calc Pi",
	cmdclass = {"build_ext": build_ext},
	ext_modules = ext_modules,
)
