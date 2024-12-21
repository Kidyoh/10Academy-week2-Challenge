from setuptools import setup, find_packages

setup(
    name="tellco_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'streamlit',
        'plotly',
        'scikit-learn',
        'python-dotenv'
    ]
) 