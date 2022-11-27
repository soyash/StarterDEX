// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract WheatToken is ERC20 {

    constructor() ERC20("WheatToken", "WHEAT") {}

    function mint(uint amount) public payable {
        _mint(msg.sender, amount);
    }
}