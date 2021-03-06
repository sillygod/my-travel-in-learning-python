#! /user/bin/python

"""This is a simple implement 2d vector by c++,
about the vector_wrap.cxx. It is produced by swig.
"""


from distutils.core import setup, Extension

vector_module = Extension(
    '_elements',
    sources=['elements_wrap.cxx', 'elements.cpp'],
)


setup(
    name='object',
    version='0.3',
    author='sillygod',
    description="""a simple test wrap c++ code for python use""",
    ext_modules=[vector_module],
    # py_modules=['vector']
)
