import pytest

@pytest.fixture(scope='function', autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass

@pytest.fixture(scope='module')
def wheatToken(WheatToken, accounts):
    return WheatToken.deploy({'from':accounts[0]})

@pytest.fixture(scope='module')
def dex(wheatToken, DEX, accounts):
    # tested this approach it works
    token_address = wheatToken.address
    return DEX.deploy(token_address, {'from':accounts[0]})