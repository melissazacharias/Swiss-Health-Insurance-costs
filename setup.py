from setuptools import setup

setup(
    name='swisshealthinsurancecosts',
    version='0.1.0',    
    description='Analysis of swiss health insurance models.',
    url='https://github.com/shuds13/pyexample',
    author='Mélissa Zacharias',
    author_email='thegreatestaxolotl@protonmail.com',
    license='GPL-3.0 license',
    packages=['swisshealthinsurancecosts'],
    install_requires=['matplotlib',
                      'plotly',
                      'numpy',
                      'pandas',
                      'seaborn',
                      'streamlit',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.8',
    ],
)
