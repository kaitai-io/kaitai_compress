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
| [brotli](https://en.wikipedia.org/wiki/brotli) | `brotli` | compression level (`0`-`11`), mode (`generic`, `text`, `font`), log window size , log block size, dictionary | [RFC 7932](https://datatracker.ietf.org/doc/html/rfc7932) | `br` |
| [LZ4](https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)) | `lz4` | block_size, if should link blocks, compression level (`0`-`16`), if should checksum frame, if should checksum each block | [LZ4 block specification](https://lz4.github.io/lz4/lz4_Block_format.md) | `lz4` |
| [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) | `lzma` | algorithm version (`1, 2`), compression level (`0-9`, `-1` - don't compress with lzma, but use other filters specified), format (`auto`, `alone`, `raw`, `xz`), checksumming algorithm (`none`, `crc32`, `crc64`, `sha256`), modifiers (`e` for `--extreme`), dictionary size, literal context bit count, literal position bit count, position bit count, match finder (`hc3`, `hc4`, `bt2`, `bt3`, `bt4`), mode (`normal`, `fast`), additional_filters | Raw LZMA stream | `lzma` |
| [DEFLATE](https://en.wikipedia.org/wiki/DEFLATE) (AKA zlib) | `zlib` | container type (`raw`, `zlib`, `gzip`), log of window size (`9`-`15`), dictionary, compression level (`0`-`9`, `-1` for default), memory level (`0`-`9`), strategy (`filtered`, `huffman_only`), method (currently only `deflated` is supported) | [RFC 1951](https://tools.ietf.org/html/rfc1951) | `zlib`, `gz` |
| [zstd](https://zstd.net) (AKA zstandard) | `zstd` | format (`zstd1_magicless`, `zstd1`),  log of (max) window size, dictionary, compression level (`1` - `22`, `-5` - `-1`), if should write checksum, if should write uncompressed size, if should write dict ID, strategy (`fast`, `dfast`, `greedy`, `lazy`, `lazy2`, `btlazy2`, `btopt`, `btultra`, `btultra2`), hash log size, match min size, chain log size, search log size, overlap log size, target length, if should use long distance matching, ldm hash log size, ldm match min size, ldm bucket size log, ldm hash rate log, job size, force max window | [Spec & ref implementation](http://facebook.github.io/zstd/zstd_manual.html) | `zst` |
| [bzip2](https://en.wikipedia.org/wiki/bzip2) | `bz2` | compression level (`1` - `9`)   to add |[Official repo](https://gitlab.com/federicomenaquintero/bzip2)|`bz2`|
