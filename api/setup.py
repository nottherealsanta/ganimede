from setuptools import setup, find_packages

setup(
    name='ganimede',
    version='0.1.0',
    description='A Rethinking of Computational Notebooks',
    author='nottherealsanta',
    packages=find_packages( include=['ganimede', 'ganimede.*']),
    install_requires=[
        "jupyter_client>=7.4.9",
        "starlette>=0.23.1",
        "pandas>=1.5.3",
        "black>=23.1.0",
        "ipykernel>=6.20.2",
        "uvicorn>=0.20.0",
        "rich>=13.2.0",
        "websockets>=11.0.3",
        "ypy-websocket==0.12.1",
        "click==8.1.3",
    ],
    entry_points={
        'console_scripts': [
            'ganimede = ganimede.main:cli',
            'ganimede_dev = ganimede.main:dev_cli'
        ]
    },
    python_requires='>=3.8',
    include_package_data=True,
    package_data={
    "ganimede": ['ui_dist/**/*'],
    },

)