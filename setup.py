from distutils.core import setup, Extension

charutils_module = Extension('pychseg.charutils', sources = ['pychseg/extend/charutils.c'])

setup (
      name='pychseg',
      version='0.01',
      description='A Python Chinese Segment Project',
      author='Chris Song',
      author_email='fakechris@gmail.com',
      url='http://code.google.com/p/pychseg/',
      license='BSD',
      packages=['pychseg', 'pychseg.utils', 'pychseg.mmseg'],
      package_dir={'pychseg': 'pychseg'},
      package_data={'pychseg': ['wordlist/*.lex']},
      #ext_modules = [charutils_module]
)
