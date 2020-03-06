from setuptools import setup

setup(
    name='audio scatter',
    version='0.1.0',
    py_modules=['audio_scatter'],
    install_requires=[
        'seaborn>=0.9.0',
        'matplotlib>=3.1.2',
        'numpy>=1.17.4',
        'ipython>=7.11.1',
        'pandas>=0.25.3'
    ],
)
