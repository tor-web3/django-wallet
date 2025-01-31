#!/usr/bin/env python3
try:
    import config
except ImportError:
    pass


from binascii import (
    hexlify, unhexlify
)

import pytest

try:
    from hdwallet.libs.base58 import (
        check_encode, check_decode, decode, encode, string_to_int
    )
except ImportError:
    from wallet.hdwallet.libs.base58 import (
        check_encode, check_decode, decode, encode, string_to_int
    )


RAW: str = "0488ade405d5bc481680000000b5b40efbdef2e0a2e8ee6fa9d371f951f93e3b1e3c1b50fb31f9ea36cfc7c88100b9d3f3" \
           "12b38951361597219c8979e177d99349fd0213bac55508c8469d02064f"

ENCODED_RAW: str = "xpub6GzA69ujvGDmXQDwJnCnyDBr5FxBFri57tFBzD1Q3HTUkRRS35eZND12MPL1d7iXT15tLwbKmvxhJDFtExNc7SU" \
                   "efgYGNE7xCQan6Cmhp8f"


def test_base58():

    assert check_encode(raw=unhexlify(RAW)) == "xprvA3zogeNr5tfUJv9UCkfnc5F7XE7grPzDkfKbBpbnUwvVsd6HVYLJp" \
                                               "QgYWCBjXwZw3GdtSVUQ7BDEgmi6MHt4MatV9gDtWuJuGYhYL7nj6aa"

    assert hexlify(check_decode(enc=ENCODED_RAW)).decode() == \
        "0488b21e05d5bc481680000000b5b40efbdef2e0a2e8ee6fa9d371f951f93e3b1e3c1b50fb31f9ea36cfc7c88100b9d3" \
        "f312b38951361597219c8979e177d99349fd0213bac55508c8469d02064f"

    with pytest.raises(TypeError, match="string argument without an encoding"):
        assert string_to_int(str("meherett"))


    assert decode("111233QC4") == b'\x00\x00\x00(\x7f\xb4\xcd'


    assert encode(decode("111233QC4")) == "111233QC4"

    # Tron 地址转换
    # TUD4YXYdj2t1gP5th3A7t97mx1AUmrrQRt
    # 41C81107148E5FA4B4A2EDF3D5354DB6C6BE5B5549
    assert check_encode(b'A\xc8\x11\x07\x14\x8e_\xa4\xb4\xa2\xed\xf3\xd55M\xb6\xc6\xbe[UI') == "TUD4YXYdj2t1gP5th3A7t97mx1AUmrrQRt"
