from setuptools import setup, find_packages

setup(
    name="netmind",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scapy>=2.5.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "netmind=src.ui.cli:main",
        ],
    },
    author="Falconmx1",
    description="Herramienta de red con IA para análisis y detección de anomalías",
    license="MIT",
)
