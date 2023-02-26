from library import getAmountOut, getAmountIn
from brownie import *
from fractions import Fraction
from scipy import optimize


def calc_profit(borrow_amount):
    """USER'S NOTE: x0a, y0a, x0b, and y0b must be defined before calling calc_profit()"""
    # get repayment INPUT at borrow_amount OUTPUT
    # x0a and y0a are the reserves of the liquidity pool from which the token is borrowed
    # x0b and y0b are the reserves of the liquidity pool where the tokens are swapped before flash repayment
    flash_repay_amount = getAmountIn(
        reserves_token0=x0a,
        reserves_token1=y0a,
        fee=Fraction(3, 1000),
        token_out_quantity=borrow_amount,
        token_in="token0",
    )

    swap_amount_out = getAmountOut(
        reserves_token0=x0b,
        reserves_token1=y0b,
        fee=Fraction(3, 1000),
        token_in_quantity=borrow_amount,
        token_in="token1",
    )

    return swap_amount_out - flash_repay_amount


def getOptimumBorrow(x0a, y0a, x0b, y0b):

    bounds = (1, float(y0a))
    bracket = (0.01 * y0a, 0.05 * y0a)

    result = optimize.minimize_scalar(
        lambda x: -float(calc_profit(borrow_amount=x)),
        method="bounded",
        bounds=bounds,
        bracket=bracket,
    )

    return result.x, -result.fun


# Define Here
x0a = None
y0a = None
x0b = None
y0b = None
