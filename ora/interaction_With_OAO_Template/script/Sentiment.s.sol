// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script} from "forge-std/Script.sol";
import {Sentiment} from "../src/sentiment.sol";
import {IAIOracle} from "OAO/contracts/interfaces/IAIOracle.sol";

contract SentimentScript is Script {
    address OAO_PROXY;

    function setUp() public {
        OAO_PROXY = 0x0A0f4321214BB6C7811dD8a71cF587bdaF03f0A0;
    }

    function run() public {
        uint privateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(privateKey);
        new Sentiment(IAIOracle(OAO_PROXY));
        vm.stopBroadcast();
    }
}