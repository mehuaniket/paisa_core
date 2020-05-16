from setuptools import setup

setup(
    name='paisa_core',
    version='0.1.0',
    packages=['paisa_core'],
    url='https://github.com/kodani/paisa_core',
    license='AGPL-3.0',
    author='Aniket Patel',
    author_email='patelaniket165@gmail.com',
    description='Python SDK for5 Paisa trading APIs',
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: AGPL-3.0 License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=[
        "requests>=2.18.4",
        "six>=1.11.0",
        "pyOpenSSL>=17.5.0",
        "enum34>=1.1.6",
        "python-dateutil>=2.6.1",
        "autobahn[twisted]>=17.10.1",
        "netifaces>=0.10.9",
        "pbkdf2>=1.3",
        "pycrypto>=2.6.1",
        "requests>=2.22.0",
        "urllib3>=1.25.7",
        "pycryptodome>=3.4.3"
    ],
    setup_requires=[
        "requests",
        "six",
        "pyOpenSSL",
        "enum34",
        "python-dateutil",
        "autobahn[twisted]",
        "netifaces",
        "pbkdf2",
        "pycrypto",
        "requests",
        "urllib3",
        "pycryptodome"
    ]
)
