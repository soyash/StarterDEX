// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";`
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract DEX {

    using SafeMath for uint256;
    IERC20 token; // instantiating imported contract

    uint256 public totalLiquidity;
    mapping (address => uint256) public lpToLiquidiy; // liquidity provided by individual users

    mapping (address => uint256) public tokenToLiquidity;

    // emitted when ETH is swaped for a token i.e. Token bought
    event EthToTokenSwap();

    // emitted when ETH is swaped for a token i.e. Token bought
    event TokenToEthSwap();

    // liquidity provided to DEX - could be sending contract ETH but depends on implementation
    event LiquidityProvided();

    event LiquidityRemoved();

    constructor(address _token) {
        token = IERC20(_token); // specifying the tokens we want to use for swapping - here _token is address of WHEAT
    }

    // liq providers calls this function with ETH to provide initial liquidity
    function init(uint256 amount) public payable returns(uint256) {
        require(totalLiquidity == 0, "DEX has already been initialized!");
        totalLiquidity = address(this).balance;
        // caller of init is address[0] (msg.sender) but caller of token.transfer will be contract (address(this)) hence transferFrom
        require(token.transferFrom(msg.sender, address(this), amount), "Wheat token transfer failed, unable to initialize contract!");
        return totalLiquidity;
    }


    function price(uint256 xInput, uint256 xReserves, uint256 yReserves) public view returns(uint256 yOutput) {
        uint256 xInputWithFee = xInput.mul(997);
        uint256 numerator = xInputWithFee.mul(yReserves);
        // using 997 in numerator and 1000 in denominator multiplies the result by 0.3% incorporating fee
        uint256 denominator = (xReserves.mul(1000)).add(xInputWithFee);
        return (numerator / denominator);
        // yOuput = ((xInput * yReserves) / xReserves); logically this is what is going on rest is added for fees
    }


    function ethToToken() public payable returns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 tokens_bought = price(msg.value, address(this).balance.sub(msg.value), token_reserve);
        require(token.transfer(msg.sender, tokens_bought), "ETH to Token swap failed!");
        return tokens_bought;
    }


    function tokenToEth(uint256 tokens) public returns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 eth_bought = price(tokens, token_reserve, address(this).balance);
        payable(msg.sender).transfer(eth_bought);
        require(token.transferFrom(msg.sender, address(this), tokens), "Token to ETH swap failed to send tokens!");
        return eth_bought;
    }


    function depositLiquidity() public payable returns (uint256) {
        // first function takes some ETH from user
        require(msg.value > 0, "Non zero ETH needs to be deposited");
        uint256 initialRatio = (address(this).balance / token.balanceOf(address(this)));
        return initialRatio;
        // then also takes required amount of token being deposited
        // updates any mappings that track user provided liquidity
    }

    function deposit() public payable returns (uint256) {
        uint256 eth_reserve = address(this).balance.sub(msg.value);
        uint256 token_reserve = token.balanceOf(address(this));

        uint256 token_amount = (msg.value.mul(token_reserve) / eth_reserve).add(1);

        uint256 liquidity_minted = msg.value.mul(totalLiquidity) / eth_reserve;
        liquidity[msg.sender] = liquidity[msg.sender].add(liquidity_minted);
        totalLiquidity = totalLiquidity.add(liquidity_minted);
        require(token.transferFrom(msg.sender, address(this), token_amount));
        return liquidity_minted;
    }

    function withdraw(uint256 amount) public returns (uint256, uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 eth_amount = amount.mul(address(this).balance) / totalLiquidity;
        uint256 token_amount = amount.mul(token_reserve) / totalLiquidity;
        liquidity[msg.sender] = liquidity[msg.sender].sub(eth_amount);
        totalLiquidity = totalLiquidity.sub(eth_amount);
        msg.sender.transfer(eth_amount);
        require(token.transfer(msg.sender, token_amount));
        return (eth_amount, token_amount);
    }
}