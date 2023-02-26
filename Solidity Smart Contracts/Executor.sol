// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// payload executor contract, has capability to send raw calldata to one or multiple addresses
contract Executor {
    address owner;

    constructor() {
        owner = msg.sender;
    }

    // used for executePayloads()
    struct payload {
        address target;
        bytes callData;
        uint256 value;
    }

    // only owner of contract can execute payloads
    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    // executes a single payload
    function execute(
        address _target,
        bytes memory _payload
    ) public payable returns (bool _success, bytes memory response) {
        return _target.call{value: msg.value}(_payload);
    }

    // executes multiple payloads
    function executePayloads(payload[] memory _payloads) public payable {
        for (uint i = 0; i < _payloads.length; i++) {
            (bool success, bytes memory response) = _payloads[i].target.call{
                value: _payloads[i].value
            }(_payloads[i].callData);
            // tx will fail if a single payload fails
            require(success == true, "payload failed");
        }
    }
}
