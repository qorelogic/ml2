
# python setup2.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
	Extension("ccalcpi",
		["ccalcpi.pyx"],
		extra_compile_args = ["-O3", "-ffast-math", "-march=native"],
		extra_link_args = ["-fopenmp"],
	)
]

setup(
	name = "Calc Pi",
	cmdclass = {"build_ext": build_ext},
	ext_modules = ext_modules,
)
