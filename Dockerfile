FROM debian:bullseye-slim as base

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="Christian Schulz <christian.schulz@ufz.de> \
        Martin Abbrent <martin.abbrent@ufz.de>" \
    org.opencontainers.image.title="TSM Frontend" \
    org.opencontainers.image.licenses="HEESIL" \
    org.opencontainers.image.version="0.0.1" \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.created=$BUILD_DATE

RUN apt-get -y update \
    && apt-get -y dist-upgrade \
    && apt-get -y --no-install-recommends install \
      python3 \
      python3-pkg-resources \
      ca-certificates \
    && apt-get -y autoremove \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt

FROM base as build

RUN apt-get -y update \
    && apt-get -y --no-install-recommends install \
      python3-pip

# add requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
    && pip install \
        --user \
        --no-cache-dir \
        --no-warn-script-location -r \
        /tmp/requirements.txt

FROM base as dist

# Create a group and user
RUN useradd --uid 1000 -m appuser

# Copy python requirements build in previous stage
COPY --chown=appuser --from=build /root/.local /home/appuser/.local

# Tell docker that all future commands should run as the appuser user
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
# ENV PYTHONDONTWRITEBYTECODE=1 # Why not?
ENV PYTHONUNBUFFERED=1

COPY --chown=appuser . /home/appuser/app/

WORKDIR /home/appuser/app/
# RUN python3 manage.py collectstatic
ENTRYPOINT ["python3", "manage.py"]

