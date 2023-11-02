
# Image build arguments:
ARG baseimageversion=v2.1.2

# Base image:
FROM ghcr.io/fluxcd/flux-cli:${baseimageversion}

ENTRYPOINT /bin/sh
