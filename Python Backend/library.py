# File will contain functions commonly used functions
from brownie import Contract, network, web3, accounts


def getAmountIn(
    reserves_token0,
    reserves_token1,
    fee,
    token_out_quantity,
    token_in,
):
    """
    Calculates the required token INPUT of token_in for a target OUTPUT at current pool reserves.
    Uses the self.token0 and self.token1 pointers to determine which token is being swapped in
    and uses the appropriate formula

    Assumes token_in is token0, token_out is token1
    """

    if token_in == "token0":
        return int(
            (reserves_token0 * token_out_quantity)
            // ((1 - fee) * (reserves_token1 - token_out_quantity))
            + 1
        )

    if token_in == "token1":
        return int(
            (reserves_token1 * token_out_quantity)
            // ((1 - fee) * (reserves_token0 - token_out_quantity))
            + 1
        )


def getAmountOut(
    reserves_token0,
    reserves_token1,
    fee,
    token_in_quantity,
    token_in,
):
    """
    Calculates the expected token OUTPUT for a target INPUT at current pool reserves.
    Uses the self.token0 and self.token1 pointers to determine which token is being swapped in
    and uses the appropriate formula

    Assumes token_in is token1, token_out is token0
    """

    if token_in == "token0":
        return int(reserves_token1 * token_in_quantity * (1 - fee)) // int(
            reserves_token0 + token_in_quantity * (1 - fee)
        )

    if token_in == "token1":
        return int(reserves_token0 * token_in_quantity * (1 - fee)) // int(
            reserves_token1 + token_in_quantity * (1 - fee)
        )


def getWeb3ContractObject(address):
    """returns a web3 contract object, commonly used to get raw calldata of a function to execute payloads"""
    contract_brownie = Contract.from_explorer(address)
    return web3.eth.contract(address=address, abi=contract_brownie.abi)
