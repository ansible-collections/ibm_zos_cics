# ---------------------------------------------------------------------------- #
#                   Docker Image for Testing Environment                       #
# ---------------------------------------------------------------------------- #
FROM python:3.7-slim-buster
WORKDIR /usr/src/app
# ARG SRC
# Collection author
# ARG AUTHOR
# Collection name
# ARG COLLECTION
# Target host address
# ARG TARGET_HOST
# Private key contents that can be used to connect to TARGET_HOST
# ARG TARGET_HOST_PRIVATE_KEY

# ARG ROOT=./tmp/ansible_collections/${AUTHOR}/${COLLECTION}
# ------------- Environment Variables ------------- #
# Path to Ansible modules
ENV ANSIBLE_LIBRARY=${ROOT}/plugins/modules/
# Path to Ansible config
ENV ANSIBLE_CONFIG=${ROOT}/tests/ansible.cfg
# --------------------------- Package installation Stage 1 --------------------------- #
# Copy source into container
# COPY ${SRC} ${ROOT}
RUN apt-get update && apt-get install -y gnupg2 git python3-pip openssh-client
# --------------------------- Package installation Stage 2 --------------------------- #
# Update package info, install ansible and openssh
# RUN cd ${ROOT} && ansible-galaxy collection build . --force && ansible-galaxy collection install ${AUTHOR}-${COLLECTION}* --force -p . && cd ansible_collections/${AUTHOR}/${COLLECTION}/ && ansible-test sanity --requirements || true
# -------------------- Map UID and GID to Jenkins host IDs ------------------- #
ARG UNAME=jenkins
ARG UID=114
ARG GID=121
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER ${UNAME}
ENV PATH="/home/jenkins/.local/bin:${PATH}"
# ----------------------------- Configure SSH key ---------------------------- #
# RUN mkdir -p /home/jenkins/.ssh/
# COPY --chown=jenkins:jenkins ${TARGET_HOST_PRIVATE_KEY} /home/jenkins/.ssh/id_rsa
# COPY --chown=jenkins:jenkins configuration.yml ./
# Add SSH key to system and ensure domain is accepted
# RUN chmod 600 /home/jenkins/.ssh/id_rsa && \
#     touch /home/jenkins/.ssh/known_hosts && \
#     ssh-keyscan "${TARGET_HOST}" >> /home/jenkins/.ssh/known_hosts
