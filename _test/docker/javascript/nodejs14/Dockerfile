# Dirs expected to be shared with this container:
#
# * /kaitai_compress - Kaitai Compress repo

FROM kaitai-compress-test-base-ubuntu_18.04:latest

# curl is needed to download install.sh
# make, g++, python3 is required by npm modules install (node-gyp)
RUN apt-get install -y \
	curl \
	make \
        g++ \
	python3

# Ubuntu nodejs/npm packages are, sadly, way too old and broken.

# Set up nvm and use nvm to install nodejs + npm
# https://stackoverflow.com/a/66521281/487064

ENV NVM_DIR /root/.nvm
ENV NODE_VERSION 14

RUN \
	curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash && \
	. $HOME/.nvm/nvm.sh && \
	nvm install --latest-npm "$NODE_VERSION" && \
	nvm alias default "$NODE_VERSION" && \
	nvm use default && \
	DEFAULT_NODE_VERSION=$(nvm version default) && \
	ln -sf /root/.nvm/versions/node/$DEFAULT_NODE_VERSION/bin/node /usr/bin/nodejs && \
	ln -sf /root/.nvm/versions/node/$DEFAULT_NODE_VERSION/bin/node /usr/bin/node && \
	ln -sf /root/.nvm/versions/node/$DEFAULT_NODE_VERSION/bin/npm /usr/bin/npm

# Check nodejs version
RUN \
	nodejs --version && \
	nodejs --version | grep -q '^v14\.' && echo "Version check OK" || false

# Compression routines dependencies - generates /node_modules in container root
COPY package.json /
RUN pwd && ls -al && npm install

ENV JAVASCRIPT_MODULES_DIR /node_modules
WORKDIR /kaitai_compress/_test
ENTRYPOINT ["./run-javascript"]
