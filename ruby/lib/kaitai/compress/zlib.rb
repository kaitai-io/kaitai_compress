require 'zlib'

module Kaitai
  module Compress
    class Zlib
      def decode(data)
        ::Zlib::inflate(data)
      end
    end
  end
end
