FROM amazonlinux:2

WORKDIR /srv

# UPDATE CACHE AND INSTALL PACKAGES
RUN yum install -y gcc \
    gcc-c++ \
    glibc-devel \
    python37 \
    python3-devel \
    vim \
    krb5-workstation \
    python-devel \
    mysql-devel \
    make \
    tzdata \
    shadow-utils \
    binutils \
    ca-certificates && \
    update-ca-trust && \
    useradd -m appuser && \
    yum update -y && \
    yum clean all \
    && rm /usr/bin/python || true \
    && ln -s /usr/bin/python3.7 /usr/bin/python \
    && ln -s /usr/bin/pip-3.7 /usr/bin/pip

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    pip install --no-cache -U pip

RUN chown -R appuser: /srv /home/appuser /etc/ssl/ && chmod -R u+rwx /srv /etc/ssl/ && \
    chmod a-rwx /usr/bin/env /usr/bin/modutil /usr/bin/echo /usr/bin/chmod /usr/bin/chown /usr/bin/chgrp

ENV PATH="/home/appuser/.local/bin:${PATH}"

ENV TZ America/Sao_Paulo
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8

ENV PIP_CONFIG_FILE=/srv/pip.conf

ADD . /srv

RUN python --version

RUN pip --version

RUN pip install -r requirements.txt