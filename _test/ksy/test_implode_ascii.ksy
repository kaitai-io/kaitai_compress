meta:
  id: test_implode_ascii
seq:
  - id: body
    size-eos: true
    process: kaitai.compress.implode(4096, 1)
