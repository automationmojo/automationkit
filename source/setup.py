#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

AKIT_VERSION = '0.3'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

DEPENDENCIES = [
      "rope",
      "debugpy",
      "docutils<0.17",
      "myst-parser",
      "sphinx",
      "sphinx_rtd_theme",
      "click<8.0",
      "coverage",
      "cython",
      "ipython",
      "netifaces",
      "pyserial",
      "pycrunch-trace",
      "paramiko",
      "psycopg2",
      "pylint",
      "pyreadline3",
      "requests",
      "zeroconf",
      "rich",
      "SQLAlchemy",
      "SQLAlchemy-Utils",
      "ssdp",
      "pyyaml",
      "dlipower",
      "gunicorn",
      "jinja2",
      "werkzeug==2.0.1",
      "flask",
      "flask-migrate",
      "flask-restx"
]

DEPENDENCY_LINKS = []

setup(name='automationkit',
      version=AKIT_VERSION,
      description='Automation Kit',
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author='Myron Walker',
      author_email='myron.walker@automationmojo.com',
      url='https://automationmojo.com/automationkit',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
      ],
      project_urls={
        'Documentation': 'https://automationmojo.com/automationkit/docs',
        'Patreon': 'https://www.patreon.com/automationmojo',
        'Source': 'https://github.com/automationmojo/automationkit',
        'Tracker': 'https://github.com/automationmojo/automationkit/issues',
      },
      package_dir={'': 'packages'},
      package_data={
          '': [
              '*.css',
              '*.html',
              '*.js',
              'monitor_pid'
          ]
      },
      packages=find_namespace_packages(where='packages'),
      python_requires=">=3.8",
      install_requires=DEPENDENCIES,
      dependency_links=DEPENDENCY_LINKS,
      entry_points = {
            "console_scripts": [
                  "akit = akit.cli.akitcommand:akit_root_command"
            ]
      }
)
