
from setuptools import setup, find_packages

setup(name='django-megaraetc',
      version='0.1.dev0',
      description='MEGARA Exposure Time Calculator',
      url='https://guaix.fis.ucm.es/projects/megara/',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.4",
         'Development Status :: 3 - Alpha',
         "Environment :: Web Environment",
         'Framework :: Django',
         "Intended Audience :: Science/Research",
         "License :: OSI Approved :: GNU General Public License (GPL)",
         "Operating System :: OS Independent",
         "Topic :: Scientific/Engineering :: Astronomy",
         'Topic :: Internet :: WWW/HTTP',
         'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
         ],
      long_description=open('README.rst').read()
     )

