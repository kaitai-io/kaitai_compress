# Dirs expected to be shared with this container:
#
# * /kaitai_compress - Kaitai Compress repo

FROM kaitai-compress-test-base-ubuntu_18.04:latest

# Ruby testing dependencies
RUN gem install --no-rdoc --no-ri rspec
RUN gem install --no-rdoc --no-ri kaitai-struct

# Install prerequisites to build native code
RUN apt-get install -y \
	ruby-dev \
	build-essential \
	zlib1g-dev \
	libc6-dev \
	autoconf \
	automake \
	libtool

# Compression routines dependencies
RUN gem install --no-rdoc --no-ri extlz4
RUN gem install --no-rdoc --no-ri ruby-xz --version '>= 1'
RUN gem install --no-rdoc --no-ri zstd-ruby
RUN gem install --no-rdoc --no-ri brotli

# Check ruby version
RUN \
	ruby --version && \
	ruby --version | grep -q '^ruby 2\.5' && echo "Version check OK" || false

WORKDIR /kaitai_compress/_test
ENTRYPOINT ["rspec", "run-ruby"]
