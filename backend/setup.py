from setuptools import setup, find_packages

setup(
    name="credlens",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'google-cloud-aiplatform',
        'google-cloud-storage',
        'joblib',
        'sentence-transformers',
        'torch',
        'requests',
        'beautifulsoup4'
    ]
)