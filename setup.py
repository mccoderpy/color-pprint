from setuptools import setup

setup(
    name='color-pprint',
    version='0.0.1',
    url='https://github.com/mccoderpy/color-pprint',
    project_urls={
        'Source': 'https://github.com/mccoderpy/color-pprint/',
        'Support': 'https://discord.gg/sb69muSqsg',
        'Issue Tracker': 'https://github.com/mccoderpy/color-pprint/issues'
    },
    license='MIT',
    description='A simple package to pretty-print lists dicts, tuples, etc. with color and highlight. (documentation SOON)',
    author='mccoder.py',
    author_email='mccuber04@outlook.de',
    include_package_data=True,
    packages=['color_pprint', 'color_pprint.ansi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    install_requires=[
        'colorama>=0.3.7',
        'multidict>=5.1.0'
    ]
)
