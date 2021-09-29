# Kaitai Struct: compression processing libraries

This package provides custom processing routines to deal with
compressed binary data. Implementations are provided for:

* JavaScript
* Python
* Ruby

Note that most implementations are actually wrappers which route calls
to well-known implementations for that languages.

## Usage

To use these routines, one should add processing instruction into
.ksy file and then add relevant language-specific implementations
into one's project.

### In .ksy file

To use it, just invoke the following in your .ksy:

```
process: kaitai.compress.PROCESS_NAME(ARGUMENTS)
```

where `PROCESS_NAME` and `ARGUMENTS` should be as described in the table below.

Fully working example:

```yaml
meta:
  id: example_lz4
seq:
  - id: buf
    size: 50
    process: kaitai.compress.lz4
```

### In JavaScript / Node

Add [javascript/](https://github.com/kaitai-io/kaitai_compress/tree/master/javascript) to one's `NODE_PATH`.

### In Python

Add [python/](https://github.com/kaitai-io/kaitai_compress/tree/master/python) to one's `PYTHONPATH`.

### In Ruby

Add [ruby/lib/](https://github.com/kaitai-io/kaitai_compress/tree/master/ruby/lib/) to one's `$LOAD_PATH`.

## Supported algorithms

| Algorithm | Process name | Arguments | Conforming | Test file extension |
| - | - | - | - | - |
| [Brotli](https://en.wikipedia.org/wiki/Brotli) | `brotli` | None | [RFC 7932](https://datatracker.ietf.org/doc/html/rfc7932) | br |
| [LZ4](https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)) | `lz4` | None | [LZ4 block specification](https://lz4.github.io/lz4/lz4_Block_format.md) | lz4 |
| [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) | `lzma_raw` | None | Raw LZMA stream | lzma_raw |
| [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) | `lzma_lzma` | None | Legacy .lzma file format (AKA alone) | lzma |
| [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) | `lzma_xz` | None | .xz file format | xz |
| [DEFLATE](https://en.wikipedia.org/wiki/DEFLATE) (AKA zlib) | `zlib` | None | [RFC 1951](https://tools.ietf.org/html/rfc1951) | zlib |
| [zstd](https://zstd.net) (AKA zstandard) | `zstd` | None | [Spec & ref implementation](http://facebook.github.io/zstd/zstd_manual.html) | zst |
