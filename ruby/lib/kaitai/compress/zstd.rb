# RubyGems: zstd-ruby
require 'zstd-ruby'

module Kaitai
  module Compress
    class Zstd
      def decode(data)
        ::Zstd::decompress(data)
      end
    end
  end
end
