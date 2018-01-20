from setuptools import setup

setup(
    name='Bots-CLI',
    verions='0.1',
    py_modules=['app']
    install_requires=[
        'arrow==0.12.0',
        'click==6.0',
        'paho-mqtt==1.3.1'
    ],
    entry_points='''
        [console_scripts]
        bots=app:cli
    '''
)
