# Base image - vanilla Ubuntu 18.04 with some fixes

FROM ubuntu:18.04

# Install apt prereqs
RUN apt-get update

# Universal requirements for all CI scripts
RUN apt-get install -y --no-install-recommends \
	locales \
	ruby

# Fix locales
RUN \
	echo 'en_US.UTF-8 UTF-8' >/etc/locale.gen && \
	echo 'LANG="en_US.UTF-8"' >/etc/default/locale && \
	dpkg-reconfigure --frontend=noninteractive locales

ENV LANG en_US.UTF-8
