from setuptools import setup

setup(
    name='color-pprint',
    version='0.0.1',
    packages=['color_pprint', 'color_pprint.ansi'],
    url='https://github.com/mccoderpy/color-pprint',
    license='MIT',
    author='mccoder.py',
    author_email='mccuber04@outlook.de',
    description='A  simple package to pretty-print lists dicts, tuples, etc. with color and highlight.',
    include_package_data=True,
    install_requires=[
        'colorama>=0.3.7',
        'multidict>=5.1.0'
    ]
)
