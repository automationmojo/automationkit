
#######################################################################
#  Base image with the core OS packages and environment
#######################################################################
FROM ubuntu:18.04

ARG LANDSCAPE=landscape.yaml

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-get install -y build-essential

#######################################################################
#  Install Python 3.8 Environment
#
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install -y python3.8 python3.8-dev python3.8-venv python3-setuptools python3-pip

#######################################################################
#  Install the system dependencies for the AutomationKit
#
RUN apt-get install -y postgresql postgresql-contrib libpq-dev
RUN apt-get install -y virtualenv

#######################################################################
#  Install the AutomationKit or core automation code from the repo
#
RUN python3 -m pip install git+https://github.com/automationmojo/automationkit.git

#######################################################################
#
#
ENV AKIT_DIRECTORY=/akit
ENV AKIT_LANDSCAPE=/akit/config/${LANDSCAPE}