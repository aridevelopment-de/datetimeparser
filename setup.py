from distutils.core import setup

# for the readme
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
  name='python-datetimeparser',
  long_description_content_type="text/markdown",
  long_description=long_description,
  packages=['datetimeparser'],
  version='0.4rc',  # version number: https://peps.python.org/pep-0440/
  license='MIT',
  description='A parser library built for parsing the english language into datetime objects.',
  author='Ari24',
  author_email='ari.publicmail@gmail.com',
  url='https://github.com/aridevelopment-de/datetimeparser',
  download_url='https://github.com/aridevelopment-de/datetimeparser/archive/v0.1e.tar.gz',
  keywords=['datetime', 'parser', 'parsing', 'grammar', 'datetime-parser'],
  install_requires=[
          'python-dateutil',
          'pytz',
          'typing'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
)
