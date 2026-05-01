FROM alpine/kubectl:1.35.4@sha256:9ccd823647622b620dce092d0f1406b8b41d152ce08ac963e3d4683770b14dfd AS kubectl
FROM alpine/helm:4.1.4@sha256:4b0bdd2cf18ff6bca12aba0b2c5671384dab5035c19c57f0c58b854a0baf65be AS helm
FROM ghcr.io/astral-sh/uv:0.11.8@sha256:3b7b60a81d3c57ef471703e5c83fd4aaa33abcd403596fb22ab07db85ae91347 AS uv
FROM python:3.14-slim

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
