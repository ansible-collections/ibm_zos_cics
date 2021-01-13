# ---------------------------------------------------------------------------- #
#                   Docker Image for Testing Environment                       #
# ---------------------------------------------------------------------------- #
FROM python:3.8-buster
ENV APPDIR=/usr/src/app
WORKDIR ${APPDIR}
RUN apt-get update && apt-get install -y gnupg2 git python-pip python3-pip openssh-client && python2.7 -m pip install virtualenv && python2.7 -m virtualenv venv2 && python3.8 -m venv venv3
ENV CMCI_PYTHON_27=${APPDIR}/venv2
ENV CMCI_PYTHON_38=${APPDIR}/venv3
# -------------------- Map UID and GID to Jenkins host IDs ------------------- #
ARG UNAME=jenkins
ARG UID=114
ARG GID=121
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER ${UNAME}
ENV PATH="/home/jenkins/.local/bin:${PATH}"