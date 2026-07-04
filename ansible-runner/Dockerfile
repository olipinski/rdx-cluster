FROM alpine/kubectl:1.36.2@sha256:8c1459287ab748db6c8601ca23e91ba43ef20e1dcb83ad61f2e8e162d05fb325 AS kubectl
FROM alpine/helm:4.2.0 AS helm
FROM ghcr.io/astral-sh/uv:0.11.26@sha256:3d868e555f8f1dbc324afa005066cd11e1053fc4743b9808ca8025283e65efa5 AS uv
FROM python:3.14-slim@sha256:b877e50bd90de10af8d82c57a022fc2e0dc731c5320d762a27986facfc3355c1

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
