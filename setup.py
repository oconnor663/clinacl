import setuptools

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

setuptools.setup(
    name='clinacl',
    description='A command line tool for playing with NaCl',
    version="0.1.0",
    url='https://github.com/oconnor663/clinacl',
    author="Jack O'Connor <oconnor663@gmail.com>",
    license='MIT',
    py_modules=['clinacl'],
    entry_points={
        'console_scripts': [
            'clinacl = clinacl:main',
        ]
    },
    install_requires=['docopt', 'u-msgpack-python', 'pynacl']
)
