# docker build --progress=plain --no-cache -t kavehbc/qrcode-barcode .
# docker save -o qrcode-barcode.tar kavehbc/qrcode-barcode
# docker load --input qrcode-barcode.tar

FROM continuumio/miniconda3 AS build

# Updating conda
RUN conda update -n base -c defaults conda
# Installing git in case required by conda
RUN apt install git

WORKDIR /app
COPY . .

# Creating the environment
RUN conda env create -f _environment.yml

# Installing conda-pack
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone environment
# in /venv:
RUN conda-pack -n qr-barcode -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in the same path it'll be in the final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# RUN conda clean -a -y

# The runtime-stage image
FROM debian:buster AS runtime
LABEL version="2.0.0"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/qr-barcode-generator"
LABEL description="QR Code and Barcode Generator"

# Copy /venv from the previous stage
COPY --from=build /venv /venv

# Copy /app from the previous stage
COPY --from=build /app /app

WORKDIR /app
EXPOSE 8501

# Run the code with the environment activated
SHELL ["/bin/bash", "-c"]

# change file permission to prevent access denied error
RUN chmod +x run.bash

ENTRYPOINT ["./run.bash"]