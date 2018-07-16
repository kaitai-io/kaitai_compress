# RubyGems: extlz4
require 'extlz4'

module Kaitai
  module Compress
    class Lz4
      def decode(data)
        LZ4::decode(data)
      end
    end
  end
end
