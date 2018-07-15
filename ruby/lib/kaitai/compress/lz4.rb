require 'lz4-ruby'

module Kaitai
  module Compress
    class Lz4
      def decode(data)
        LZ4::decompress(data)
      end
    end
  end
end
