ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}

SHELL [ "/bin/bash", "-c" ]

ENV PYTHON_VERSION_SET=${PYTHON_VERSION}
RUN echo $PYTHON_VERSION_SET
RUN apt-get update && apt upgrade -y

COPY ./requirements.txt /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/
COPY ./dev-requirements.txt /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/

RUN pip install -r /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt

COPY ./ /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics
WORKDIR /ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics
