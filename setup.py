from setuptools import setup, find_packages

setup(name="prima_value_retriver",
      version='1.0',
      description='Prima value retriver - Etl package',
      author='Diego Paladini',
      author_email='diegopaladini@gmail.com',
      url='https://gitlab.advancedanalytics.generali.com/aa-generali-italia/portale-liquidatori-iot-microservices.git',
      install_requires=['pyyaml',
                        'python-dateutil==2.8.1',
                        'pandas==1.2.3'],
      packages=find_packages()
)