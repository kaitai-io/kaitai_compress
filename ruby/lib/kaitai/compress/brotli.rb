# RubyGems: brotli
require 'brotli'

module Kaitai
  module Compress
    class Brotli
      def decode(data)
        ::Brotli::inflate(data)
      end
    end
  end
end
