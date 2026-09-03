FROM alpine/kubectl:1.36.3@sha256:dae261106d5555008acede256b7102c8a6decde7209198434f5999f051460f57 AS kubectl
FROM alpine/helm:4.2.0@sha256:af08f75a3130d666a50b9fc150f40987ef20b885cf67659aabf4b83a5f2c5501 AS helm
FROM ghcr.io/astral-sh/uv:0.12.4@sha256:d0a6eca6c669dc7e9c51218707b8438a3d30402733d739dcc00adb3e213e8f5c AS uv
FROM python:3.14-slim@sha256:ce40764625a4ff50df3548277632e7f96c4e77fe75fa848aae9885476e7df5a4

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/runner/.venv

COPY --from=uv /uv /uvx /usr/local/bin/
COPY --from=kubectl /usr/local/bin/kubectl /usr/local/bin/kubectl
COPY --from=helm /usr/bin/helm /usr/local/bin/helm

RUN apt update -qq && \
    apt install sudo git apt-utils pwgen gnupg curl wireguard-tools vim whois wget jq awscli watch -y && \
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
