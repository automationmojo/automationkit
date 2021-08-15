#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

DEPENDENCIES = [
      "rope",
      "debugpy",
      "docutils<0.17",
      "sphinx",
      "sphinx_rtd_theme",
      "click",
      "coverage",
      "ipython",
      "netifaces",
      "pyserial",
      "paramiko",
      "psycopg2",
      "pylint",
      "requests",
      "SQLAlchemy==1.3.20",
      "SQLAlchemy-Utils",
      "ssdp",
      "pyyaml",
      "dlipower",
      "gunicorn",
      "werkzeug==2.0.1",
      "flask",
      "flask-restplus"
]

DEPENDENCY_LINKS = []

setup(name='akit',
      version='1.0',
      description='Automation Kit',
      author='Myron Walker',
      author_email='myron.walker@automationmojo.com',
      url='https://automationmojo.com/products/akit',
      package_dir={'': 'packages'},
      package_data={'': ['*.html']},
      packages=find_namespace_packages(where='packages'),
      install_requires=DEPENDENCIES,
      dependency_links=DEPENDENCY_LINKS,
      entry_points = {
            "console_scripts": [
                  "akit = akit.cli.akitcommand:akit_root_command"
            ]
      }
)
