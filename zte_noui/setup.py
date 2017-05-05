from distutils.core import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

import os
os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"
Options.embed = "main"

setup(
  name = 'Dikjstra',
  ext_modules = cythonize("dijkstra.pyx"),
)

setup(ext_modules = cythonize(
           "dijkstra.pyx",                 # our Cython source
           sources=[],  # additional source file(s)
           language="c++",             # generate C++ code
      ))
