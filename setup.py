from setuptools import find_packages
from setuptools import setup


setup(
    author='Marcus Lugg',
    author_email='marcuslugg@googlemail.com',
    description='Measure the local air quality index (AQI) based on PM2.5 and PM10 concentrations.',
    install_requires=[
        'pyserial<4',
        'seaborn'
    ],
    extras_require={
        'development': [
            'pytest'
        ]
    },
    license='',
    name='aqi',
    packages=find_packages(),
    url='https://github.com/cortadocodes/aqi',
    version='0.1.0',
)
