FROM alpine:latest

# based on https://hub.docker.com/r/rosstimson/packer/~/dockerfile/
ENV PACKER_VERSION 0.10.0

# Download and install Packer.
RUN mkdir /tmp/packer \
    && cd /tmp/packer \
    && apk add --update bash curl ca-certificates openssh-client git unzip jq \
    && curl -O -sS -L https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip \
    && unzip packer_${PACKER_VERSION}_linux_amd64.zip \
    && apk del unzip \
    && mv packer* /usr/local/bin \
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/packer

# for jq
ENV PATH=/usr/local/bin:$PATH

# install asserts
ADD assets/ /opt/resource/
RUN chmod +x /opt/resource/*
