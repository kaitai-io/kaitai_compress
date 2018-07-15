# Kaitai Struct: compression processing libraries

This package provides custom processing routines to deal with
compressed binary data. Implementations are provided for:

* Python
* Ruby

Note that most implementations are actually wrappers which route calls
to well-known implementations for that languages.

The following algorithms are supported:

## LZ4

[LZ4](https://en.wikipedia.org/wiki/LZ4_(compression_algorithm))
compression, conforming to [LZ4 block
specification](https://lz4.github.io/lz4/lz4_Block_format.md):

```yaml
process: kaitai.compress.lz4
```

## LZMA

[LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm)
compression is supported in 3 formats:

### Raw LZMA stream

```yaml
process: kaitai.compress.lzma_raw
```

### Legacy .lzma file format (AKA alone)

```yaml
process: kaitai.compress.lzma_lzma
```

### .xz file format

```yaml
process: kaitai.compress.lzma_xz
```

## DEFLATE (AKA zlib) compression

[DEFLATE streams](https://en.wikipedia.org/wiki/DEFLATE), as defined
in [RFC 1951](https://tools.ietf.org/html/rfc1951).

```yaml
process: kaitai.compress.zlib
```
