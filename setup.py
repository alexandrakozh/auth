from setuptools import setup

setup(name='MyApp',
      version='1.0',
      description='Application for Authentication',
      author='Oleksandra KOzhemiakina',
      author_email='alexkozhemiakina@gmail.com',
      packages=['auth_app'],
      include_package_data=True,
      install_requires=['flask==0.10.1', 'flask-login==0.2.7', 'sqlalchemy==0.8.2', 'flask-sqlalchemy==1.0',
                        'flask.wtf'],
      )