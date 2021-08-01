# Dirs expected to be shared with this container:
#
# * /kaitai_compress - Kaitai Compress repo

FROM kaitai-compress-test-base-ubuntu_18.04:latest

# Python 3.6 dependencies
RUN apt-get install -y --no-install-recommends \
	python3-pip

RUN pip3 install unittest-xml-reporting
RUN pip3 install setuptools

# Fix python symlink
RUN rm -f /usr/bin/python && ln -s python3 /usr/bin/python

# Check python version
RUN \
	python --version && \
	python --version | grep -q '^Python 3\.6' && echo "Version check OK" || false

# Install all compression modules
RUN apt-get install -y \
	python3-lz4

COPY requirements.txt /
RUN pip3 install -r /requirements.txt -v

WORKDIR /kaitai_compress/_test
ENTRYPOINT ["./run-python"]
