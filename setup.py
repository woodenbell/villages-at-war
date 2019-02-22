from os.path import join

from setuptools import setup, find_packages

setup(name='villages-at-war',
      version='0.0.1',
      description='Simulates war between two villages',
      url='http://github.com/woodenbell/villages-at-war',
      author='Gabriel Barbosa',
      author_email='woodenbell@protonmail.com',
      license='MIT',
      zip_safe=False,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Operating System :: OS Independent',
          'Topic :: Games/Entertainment'
      ],
      package_data={
          'villageswar': [join('res', '*')],
          '': ['README.md', 'LICENSE.txt']
      },
      entry_points={
          'console_scripts': ['villages-at-war=villageswar.main:main'],
      }
      )
