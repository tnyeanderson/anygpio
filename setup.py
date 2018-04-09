from setuptools import setup, find_packages

README = open("README.md").read()

setup(
    name='anygpio',
    version='0.1.6',
    description='Cross-Platform GPIO library for Single-Board Computers',
	keywords='gpio sbc cross platform rpi raspberry pi chip omega2 beaglebone opi nanopi pine a64 bpi'
	long_description=README,
	long_description_content_type='text/markdown',
	license='GPLv3',
    url='http://github.com/tnyeanderson/anygpio',
    author='Thomas Anderson',
    author_email='tnyeanderson@gmail.com',
    packages=find_packages(),
	python_requires='>=3',
)
