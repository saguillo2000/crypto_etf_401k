// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "OAO/contracts/interfaces/IAIOracle.sol";
import "OAO/contracts/AIOracleCallbackReceiver.sol";

contract Sentiment is AIOracleCallbackReceiver {
    event promptsUpdated(
        uint256 requestId,
        uint256 modelId,
        string input,
        string output,
        bytes callbackData
    );

    event promptRequest(
        uint256 requestId,
        address sender,
        uint256 modelId,
        string prompt
    );

    struct AIOracleRequest {
        address sender;
        uint256 modelId;
        bytes input;
        bytes output;
    }

    mapping(uint256 => AIOracleRequest) public requests;

    mapping(uint256 => uint64) public callbackGasLimit;

    uint256 public modelId = 11;

    constructor(IAIOracle _aiOracle) AIOracleCallbackReceiver(_aiOracle) {
        callbackGasLimit[11] = 5_000_000; // Llama
    }

    function setCallbackGasLimit(uint64 gasLimit) external {
        callbackGasLimit[modelId] = gasLimit;
    }

    mapping(uint256 => mapping(string => string)) public prompts;
    mapping(uint256 => string) public latestPrompts;
    mapping(uint256 => string) public latestResponses;

    function getLatestPrompt() external view returns (string memory) {
        return latestPrompts[modelId];
    }

    function getLatestResponse() external view returns (string memory) {
        return latestResponses[modelId];
    }

    function aiOracleCallback(
        uint256 requestId,
        bytes calldata output,
        bytes calldata callbackData
    ) external override onlyAIOracleCallback {
        AIOracleRequest storage request = requests[requestId];
        require(request.sender != address(0), "request does not exist");
        request.output = output;
        prompts[request.modelId][string(request.input)] = string(output);

        // Update latest prompt and response
        latestPrompts[request.modelId] = string(request.input);
        latestResponses[request.modelId] = string(output);

        bytes memory lowercaseOutput = bytes(toLowerCase(string(output)));
        if (keccak256(lowercaseOutput) == keccak256(bytes("negative"))) {
            sell();
        } else {
            keep();
        }

        emit promptsUpdated(
            requestId,
            request.modelId,
            string(request.input),
            string(output),
            callbackData
        );
    }

    string action = "";

    function sell() internal {
        action = "sell";
    }

    function keep() internal {
        action = "Keep";
    }

    function toLowerCase(
        string memory str
    ) internal pure returns (string memory) {
        bytes memory bStr = bytes(str);
        for (uint i = 0; i < bStr.length; i++) {
            if (uint8(bStr[i]) >= 65 && uint8(bStr[i]) <= 90) {
                bStr[i] = bytes1(uint8(bStr[i]) + 32);
            }
        }
        return string(bStr);
    }

    function getInvestmentDecision() external view returns (string memory) {
        return action;
    }

    function estimateFee() public view returns (uint256) {
        return aiOracle.estimateFee(modelId, callbackGasLimit[modelId]);
    }

    function analyzeSentiment(string calldata text) external payable {
        string memory prompt = string.concat(
            "Analyze the sentiment of the following text and respond with only 'positive' or 'negative':\n\n",
            text,
            "\n\nSentiment:"
        );

        bytes memory input = bytes(prompt);
        address callbackAddress = address(this);
        bytes memory callbackData = bytes("");
        uint256 requestId = aiOracle.requestCallback{value: msg.value}(
            modelId,
            input,
            callbackAddress,
            callbackGasLimit[modelId],
            callbackData
        );

        AIOracleRequest storage request = requests[requestId];
        request.input = input;
        request.sender = msg.sender;
        request.modelId = modelId;

        emit promptRequest(requestId, msg.sender, modelId, prompt);
    }
}
