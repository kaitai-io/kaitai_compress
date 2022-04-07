meta:
  id: test_implode_binary
seq:
  - id: body
    size-eos: true
    process: kaitai.compress.implode(4096, 0)
