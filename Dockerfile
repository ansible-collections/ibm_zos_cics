# (c) Copyright IBM Corp. 2021
# ---------------------------------------------------------------------------- #
#                   Docker Image for Testing Environment                       #
# ---------------------------------------------------------------------------- #
FROM python:3.8-buster

SHELL [ "/bin/bash", "-c" ]

RUN apt-get update && apt-get install -y gnupg2 git python-pip python3-pip openssh-client && python2.7 -m pip install virtualenv==20.4.7

RUN python3 -m venv /venv3
RUN python2.7 -m virtualenv /venv2
RUN source /venv3/bin/activate

COPY ./requirements.txt /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/
COPY ./dev-requirements.txt /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/

RUN pip install -r /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt

COPY ./ /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics
WORKDIR /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics

# -------------------- Map UID and GID to Jenkins host IDs ------------------- #
# ARG UNAME=jenkins
# ARG UID=114
# ARG GID=121
# RUN groupadd -g $GID -o $UNAME
# RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
# USER ${UNAME}
# ENV PATH="/home/jenkins/.local/bin:${PATH}"