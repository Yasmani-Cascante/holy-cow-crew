from setuptools import setup, find_packages
from pathlib import Path

# Leer README.md para descripción larga
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="holy-cow-crew",
    version="0.1.0",
    description="Sistema multi-agente para optimización de restaurantes Holy Cow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yasmani Cascante",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'crewai>=0.100.1',
        'langchain>=0.1.5',
        'pandas>=2.1.4',
        'numpy>=1.24.3',
        'python-dotenv>=1.0.0',
        'openai>=1.7.1',
        'anthropic>=0.8.0',
        'litellm>=1.10.1',
        'pydantic>=2.5.2',
        'duckduckgo-search>=3.9.3',
        'google-search-results>=2.4.2',
        'pytest>=7.0.0'
    ],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.10',
    ],
)