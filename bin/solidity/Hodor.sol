pragma solidity ^0.4.0;

contract Hodor {
    
    string greeting;
    
    function Hodor(string _greeting) {
        greeting = _greeting;
    }
    
    function greet() constant returns (string) {
        return greeting;
    }
    
    function setGreeting(string _greeting) {
        greeting = _greeting;
    }
}

