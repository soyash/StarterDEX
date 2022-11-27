def test_init(wheatToken, dex, accounts):
    initial_liquidity = dex.totalLiquidity()

    wheatToken.mint(1000, {'from':accounts[0]})
    wheatToken.approve(dex.address, 1000, {'from':accounts[0]})
    dex.init(1000, {'from':accounts[0], 'value':'1 ether'})

    final_liquidity = dex.totalLiquidity()
    #print('DEX liquidity: Ether ' + str(dex.balance()) + ' Wheat Token ' + str(wheatToken.balanceOf(dex.address)))

    assert initial_liquidity == 0
    assert final_liquidity == '1 ether'

def test_price(wheatToken, dex, accounts):
    wheatToken.mint('1000 ether', {'from':accounts[0]})
    wheatToken.approve(dex.address, '1000 ether', {'from':accounts[0]})

    # initializes with ratio ETH:WHEAT = 1000:1000
    dex.init('1000 ether', {'from':accounts[0], 'value':'1000 ether'})

    # supply 1 eth and get 1 token
    tokenValueReturned = dex.price('900 ether', '1000 ether', '1000 ether')
    print('Token Amount received: ' + str(tokenValueReturned))

    # Slippage
    #1 ether gives => .996006981039903216 tokens instead of .997
    #10 ether gives => 9.871580343970612988 tokens 
    #100 ether gives => 90.661089388014913158 tokens


def test_ethToTokenTransfer(wheatToken, dex, accounts):
    wheatToken.mint('1000 ether', {'from':accounts[0]})
    wheatToken.approve(dex.address, '1000 ether', {'from':accounts[0]})
    # initializing with ratio ETH:WHEAT = 10:1000
    dex.init('1000 ether', {'from':accounts[0], 'value':'10 ether'})

    initial_eth_balance = dex.balance()
    initial_token_balance = wheatToken.balanceOf(dex.address)

    tokensBought = dex.ethToToken({'from':accounts[0], 'value':'1 ether'})

    final_eth_balance = dex.balance()
    final_token_balance = wheatToken.balanceOf(dex.address)

    #print('WHEAT tokens bought: ' + str(tokensBought.return_value))
    #print('Initial ETH: ' + str(initial_eth_balance) + ' Final ETH: ' + str(final_eth_balance))
    #print('Initial WHEAT: ' + str(initial_token_balance) + ' Final WHEAT: ' + str(final_token_balance)) 

    # 0.01 ETH sent
    #Initial ETH: 10000000000000000000 Final ETH: 10010000000000000000
    #Initial WHEAT: 1000000000000000000000 Final WHEAT: 999003993018960096784

    # 1 ETH sent since this is 10% of total ETH liquidity we loose a lot due to slippage over the 0.3% fee
    #WHEAT tokens bought: 90661089388014913158
    #Initial ETH: 10000000000000000000 Final ETH: 11000000000000000000
    #Initial WHEAT: 1000000000000000000000 Final WHEAT: 909338910611985086842

def test_tokenToETH(wheatToken, dex, accounts):
    wheatToken.mint('1000 ether', {'from':accounts[0]})
    wheatToken.approve(dex.address, '1000 ether', {'from':accounts[0]})
    # initializing with ratio ETH:WHEAT = 5:500
    dex.init('500 ether', {'from':accounts[0], 'value':'5 ether'})

    initial_eth_balance = dex.balance()
    initial_token_balance = wheatToken.balanceOf(dex.address)

    tokensBought = dex.tokenToEth('100 ether', {'from':accounts[0]})

    final_eth_balance = dex.balance()
    final_token_balance = wheatToken.balanceOf(dex.address)

    #print('ETH tokens bought: ' + str(tokensBought.return_value))
    #print('Initial ETH: ' + str(initial_eth_balance) + ' Final ETH: ' + str(final_eth_balance))
    #print('Initial WHEAT: ' + str(initial_token_balance) + ' Final WHEAT: ' + str(final_token_balance))

    #ETH tokens bought: .831248957812239453
    #Initial ETH: 5,000000000000000000 Final ETH: 4,168751042187760547
    #Initial WHEAT: 500,000000000000000000 Final WHEAT: 600,000000000000000000

def test_depositLiquidity(wheatToken, dex, accounts):
    wheatToken.mint('100 ether', {'from':accounts[0]})
    wheatToken.approve(dex.address, '100 ether', {'from':accounts[0]})
    # initializing with ratio ETH:WHEAT = 100:100
    dex.init('10 ether', {'from':accounts[0], 'value':'100 ether'})

    initialRatio = dex.depositLiquidity({'from':accounts[0], 'value':'50 ether'})
    print(initialRatio.return_value)