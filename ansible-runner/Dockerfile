FROM alpine/kubectl:1.36.1@sha256:96744389db9cb3b5588e1015a5a0effc31cb7f24c0bb2de13a2e10dec3a1ce6b AS kubectl
FROM alpine/helm:4.2.0@sha256:af08f75a3130d666a50b9fc150f40987ef20b885cf67659aabf4b83a5f2c5501 AS helm
FROM ghcr.io/astral-sh/uv:0.11.18@sha256:78bc42400d77b0678ba95765305c826652ed5431f399257271dda681d0318f03 AS uv
FROM python:3.14-slim@sha256:c845af9399020c7e562969a13689e929074a10fd057acd1b1fad06a2fb068e97

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/runner/.venv

COPY --from=uv /uv /uvx /usr/local/bin/
COPY --from=kubectl /usr/local/bin/kubectl /usr/local/bin/kubectl
COPY --from=helm /usr/bin/helm /usr/local/bin/helm

RUN apt update -qq && \
    apt install sudo git apt-utils pwgen gnupg curl wireguard-tools vim whois wget jq -y && \
    apt clean && \
    rm -rf /usr/share/doc/* /usr/share/man/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD build /build
WORKDIR /build

# Install python dependencies
RUN uv pip install --system -r requirements.txt

# Install ansible roles/collections dependencies
RUN ansible-galaxy role install -r requirements.yml --roles-path "/usr/share/ansible/roles" --timeout 120
RUN ansible-galaxy collection install -r requirements.yml --collections-path "/usr/share/ansible/collections"

ENV USER=runner
ENV FOLDER=/home/runner
RUN /usr/sbin/groupadd $USER && \
    /usr/sbin/useradd $USER -m -d $FOLDER -g $USER -s /bin/bash && \
    echo $USER 'ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN for dir in \
      /runner \
      /var/lib/letsencrypt \
      /etc/letsencrypt \
      /var/log/letsencrypt ; \
    do mkdir -p $dir ; chown $USER:$USER $dir; chmod 775 $dir ; done

USER $USER

RUN echo "export GPG_TTY=\$(tty)" >> /home/runner/.bashrc

# Install helm required plugins
RUN helm plugin install https://github.com/databus23/helm-diff --verify=false

WORKDIR /runner
