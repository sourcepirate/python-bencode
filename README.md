##python-bencode

[![Build Status](https://travis-ci.org/plasmashadow/python-bencode.svg)](https://travis-ci.org/plasmashadow/python-bencode)

Becode Encoder and Decoder

##Installation

```

pip install python-bencode

```

##Usage

```python

from bencode import Bencoder

#encoding
built_to_bencode = [1,2,3]
strs = Bencoder.encode(built_to_bencode)

#decoding
decodable = "8:announce"
obj = Bencoder.decode(decodeable)


```


##LICENSE
BSD