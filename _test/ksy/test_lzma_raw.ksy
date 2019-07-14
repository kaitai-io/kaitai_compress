meta:
  id: test_lzma_raw
seq:
  - id: body
    size-eos: true
    process: kaitai.compress.lzma(2, 9, "raw")
