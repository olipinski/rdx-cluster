FROM golang:1.26.2-alpine@sha256:f85330846cde1e57ca9ec309382da3b8e6ae3ab943d2739500e08c86393a21b1 AS build
LABEL stage=builder

WORKDIR /k3s-mixins

COPY src/ .

RUN ls -la *

# Install required packages
RUN apk add git

# Install jsonnet and the jsonnet-bundler
RUN go install github.com/google/go-jsonnet/cmd/jsonnet@latest
RUN go install github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb@latest

# Install gojsontoyaml
RUN go install github.com/brancz/gojsontoyaml@latest

# Init Jsonnet project
RUN jb init

# Install mixinx
RUN jb install github.com/kubernetes-monitoring/kubernetes-mixin@master
RUN jb install github.com/prometheus-operator/kube-prometheus/jsonnet/kube-prometheus@main
RUN jb install github.com/povilasv/coredns-mixin@master

# RUN jsonnet main.jsonnet -J vendor > generated.json

# Create output directory for the manifest files
RUN mkdir templates

# Execute command to generate
RUN chmod +x generate.sh
RUN ./generate.sh

FROM scratch AS mixins
COPY --from=build /k3s-mixins/templates /
