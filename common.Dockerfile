ARG PYTHON_VERSION_SET

FROM python:${PYTHON_VERSION_SET}

SHELL [ "/bin/bash", "-c" ]

RUN apt-get update && apt upgrade -y

COPY ./requirements.txt /root/ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/requirements.txt
COPY ./dev-requirements.txt /root/ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt

RUN pip install -r /root/ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt

ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
ARG PYTHON_VERSION_SET
ENV PYTHON_VERSION_SET=${PYTHON_VERSION_SET}

WORKDIR /root/ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics