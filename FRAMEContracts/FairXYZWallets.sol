// SPDX-License-Identifier: MIT
// @ Fair.xyz dev

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";

contract FairXYZWallets is Ownable{
    
    address internal signer_address;

    address internal withdraw_address;

    constructor(address address_for_signer, address address_for_withdraw){
        signer_address = address_for_signer;
        withdraw_address = address_for_withdraw;
    }

    function view_signer() public view returns(address)
    {
        return(signer_address);
    }

    function view_withdraw() public view returns(address)
    {
        return(withdraw_address);
    }

    function change_signer(address new_address) public onlyOwner returns(address)
    {
        signer_address = new_address;
        return signer_address;
    }

    function change_withdraw(address new_address) public onlyOwner returns(address)
    {
        withdraw_address = new_address;
        return withdraw_address;
    }


}