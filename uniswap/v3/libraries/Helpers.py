# adapted from OpenZeppelin's overflow checks, which throw
# an exception if the input value exceeds the maximum value
# for this type

MIN_INT128 = -(2**127)
MAX_INT128 = 2**127 - 1

MAX_UINT8 = 0
MAX_UINT8 = 2**8 - 1

MIN_UINT128 = 0
MAX_UINT128 = 2**128 - 1

MIN_UINT160 = 0
MAX_UINT160 = 2**160 - 1

MIN_UINT256 = 0
MAX_UINT256 = 2**256 - 1


def mulmod(x, y, k):
    assert k != 0
    return (x * y) % k


def to_int128(x):
    assert x <= 2 ** (128 - 1)
    return x


def to_int256(x):
    assert x <= 2 ** (256 - 1)
    return x


def to_uint160(x):
    assert x <= 2 ** (160) - 1
    return x


# Generic integer "conversion" that performs no value checking to mimic Solidity's
# inline typecasting for int/uint types. Makes copy-pasting the Solidity functions
# easier since in-line casts can remain
def _int(x):
    return x


int8 = _int
int16 = _int
int24 = _int
int32 = _int
int40 = _int
int48 = _int
int56 = _int
int64 = _int
int72 = _int
int80 = _int
int88 = _int
int96 = _int
int104 = _int
int112 = _int
int120 = _int
int128 = _int
int136 = _int
int144 = _int
int152 = _int
int160 = _int
int168 = _int
int176 = _int
int184 = _int
int192 = _int
int200 = _int
int208 = _int
int216 = _int
int224 = _int
int232 = _int
int240 = _int
int248 = _int
int256 = _int


uint8 = _int
uint16 = _int
uint24 = _int
uint32 = _int
uint40 = _int
uint48 = _int
uint56 = _int
uint64 = _int
uint72 = _int
uint80 = _int
uint88 = _int
uint96 = _int
uint104 = _int
uint112 = _int
uint120 = _int
uint128 = _int
uint136 = _int
uint144 = _int
uint152 = _int
uint160 = _int
uint168 = _int
uint176 = _int
uint184 = _int
uint192 = _int
uint200 = _int
uint208 = _int
uint216 = _int
uint224 = _int
uint232 = _int
uint240 = _int
uint248 = _int
uint256 = _int
