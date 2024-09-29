meta:
  id: test_lzma_xz
seq:
  - id: body
    size-eos: true
    process: kaitai.compress.lzma(2, 9, "xz")
