from . import FixedPoint96, FullMath, UnsafeMath
from .Helpers import *
from typing import Union

# type hinting aliases
Int128 = int
Int256 = int
Uint128 = int
Uint160 = int
Uint256 = int


def getAmount0Delta(
    sqrtRatioAX96: Uint160,
    sqrtRatioBX96: Uint160,
    liquidity: Union[Int128, Uint128],
    roundUp: bool = None,
) -> Uint256:

    if roundUp is not None or MIN_UINT128 <= liquidity <= MAX_UINT128:
        if sqrtRatioAX96 > sqrtRatioBX96:
            (sqrtRatioAX96, sqrtRatioBX96) = (sqrtRatioBX96, sqrtRatioAX96)

        numerator1 = uint256(liquidity) << FixedPoint96.RESOLUTION
        numerator2 = sqrtRatioBX96 - sqrtRatioAX96

        assert sqrtRatioAX96 > 0, "FAIL!"

        return (
            UnsafeMath.divRoundingUp(
                FullMath.mulDivRoundingUp(
                    numerator1, numerator2, sqrtRatioBX96
                ),
                sqrtRatioAX96,
            )
            if roundUp
            else (FullMath.mulDiv(numerator1, numerator2, sqrtRatioBX96))
            // sqrtRatioAX96
        )
    else:
        return to_int256(
            -getAmount0Delta(
                sqrtRatioAX96, sqrtRatioBX96, uint128(-liquidity), False
            )
            if liquidity < 0
            else to_int256(
                getAmount0Delta(
                    sqrtRatioAX96, sqrtRatioBX96, uint128(liquidity), True
                )
            )
        )


def getAmount1Delta(
    sqrtRatioAX96: Uint160,
    sqrtRatioBX96: Uint160,
    liquidity: Union[Int128, Uint128],
    roundUp: bool = None,
) -> Uint256:

    if roundUp is not None or MIN_UINT128 <= liquidity <= MAX_UINT128:
        if sqrtRatioAX96 > sqrtRatioBX96:
            sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

        return (
            FullMath.mulDivRoundingUp(
                liquidity, sqrtRatioBX96 - sqrtRatioAX96, FixedPoint96.Q96
            )
            if roundUp
            else FullMath.mulDiv(
                liquidity, sqrtRatioBX96 - sqrtRatioAX96, FixedPoint96.Q96
            )
        )
    else:
        return to_int256(
            -getAmount1Delta(
                sqrtRatioAX96, sqrtRatioBX96, uint128(-liquidity), False
            )
            if liquidity < 0
            else to_int256(
                getAmount1Delta(
                    sqrtRatioAX96, sqrtRatioBX96, uint128(liquidity), True
                )
            )
        )


def getNextSqrtPriceFromAmount0RoundingUp(
    sqrtPX96: Uint160,
    liquidity: Uint128,
    amount: Uint256,
    add: bool,
) -> Uint160:
    # we short circuit amount == 0 because the result is otherwise not guaranteed to equal the input price
    if amount == 0:
        return sqrtPX96

    numerator1 = uint256(liquidity) << FixedPoint96.RESOLUTION

    if add:
        product = amount * sqrtPX96
        if product // amount == sqrtPX96:
            denominator = numerator1 + product
            if denominator >= numerator1:
                # always fits in 160 bits
                return FullMath.mulDivRoundingUp(
                    numerator1, sqrtPX96, denominator
                )

        return UnsafeMath.divRoundingUp(
            numerator1, numerator1 // sqrtPX96 + amount
        )
    else:
        product = amount * sqrtPX96
        # if the product overflows, we know the denominator underflows
        # in addition, we must check that the denominator does not underflow
        assert product // amount == sqrtPX96 and numerator1 > product, "FAIL!"
        denominator = numerator1 - product
        return to_uint160(
            FullMath.mulDivRoundingUp(numerator1, sqrtPX96, denominator)
        )


def getNextSqrtPriceFromAmount1RoundingDown(
    sqrtPX96: Uint160,
    liquidity: Uint128,
    amount: Uint256,
    add: bool,
) -> Uint160:

    if add:
        quotient = (
            (amount << FixedPoint96.RESOLUTION) // liquidity
            if amount <= 2**160 - 1
            else FullMath.mulDiv(amount, FixedPoint96.Q96, liquidity)
        )
        return to_uint160(uint256(sqrtPX96) + quotient)
    else:
        quotient = (
            UnsafeMath.divRoundingUp(
                amount << FixedPoint96.RESOLUTION, liquidity
            )
            if amount <= (2**160) - 1
            else FullMath.mulDivRoundingUp(amount, FixedPoint96.Q96, liquidity)
        )

        assert sqrtPX96 > quotient, "FAIL!"
        # always fits 160 bits
        return sqrtPX96 - quotient


def getNextSqrtPriceFromInput(
    sqrtPX96: Uint160,
    liquidity: Uint128,
    amountIn: Uint256,
    zeroForOne: bool,
) -> Uint160:

    assert sqrtPX96 > MIN_UINT160, "sqrtPX96 must be greater than 0"
    assert liquidity > MIN_UINT160, "liquidity must be greater than 0"

    # round to make sure that we don't pass the target price
    return (
        getNextSqrtPriceFromAmount0RoundingUp(
            sqrtPX96, liquidity, amountIn, True
        )
        if zeroForOne
        else getNextSqrtPriceFromAmount1RoundingDown(
            sqrtPX96, liquidity, amountIn, True
        )
    )


def getNextSqrtPriceFromOutput(
    sqrtPX96: int,
    liquidity: int,
    amountOut: int,
    zeroForOne: bool,
):
    assert sqrtPX96 > 0, "FAIL!"
    assert liquidity > 0, "FAIL!"

    # round to make sure that we pass the target price
    return (
        getNextSqrtPriceFromAmount1RoundingDown(
            sqrtPX96, liquidity, amountOut, False
        )
        if zeroForOne
        else getNextSqrtPriceFromAmount0RoundingUp(
            sqrtPX96, liquidity, amountOut, False
        )
    )
