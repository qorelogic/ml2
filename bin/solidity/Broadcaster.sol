pragma solidity ^0.4.0;

contract Broadcaster {
    
    uint public balance;
    address public chairperson;
    
    function Broadcaster() public {
        balance = 1000;
        chairperson = msg.sender;
    }
}
