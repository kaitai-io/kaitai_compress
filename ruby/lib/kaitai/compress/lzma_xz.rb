require 'xz'

module Kaitai
  module Compress
    class LzmaXz
      def decode(data)
        XZ::decompress(data)
      end
    end
  end
end
