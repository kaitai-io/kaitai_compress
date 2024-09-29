meta:
  id: test_lzma_lzma
seq:
  - id: body
    size-eos: true
    process: kaitai.compress.lzma(1, 9, "alone")
