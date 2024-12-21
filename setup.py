from setuptools import setup, find_packages

setup(
    name="tellco_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'streamlit',
        'scikit-learn',
        'python-pptx',
        'kaleido',
        'pytest',
        'python-dotenv'
    ]
) 