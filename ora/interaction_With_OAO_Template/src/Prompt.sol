// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "OAO/contracts/interfaces/IAIOracle.sol";
import "OAO/contracts/AIOracleCallbackReceiver.sol";

contract Prompt is AIOracleCallbackReceiver {
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

    uint256 public modelId = 11;

    mapping(uint256 => AIOracleRequest) public requests;

    mapping(uint256 => uint64) public callbackGasLimit;

    mapping(uint256 => string) public latestPrompts;
    mapping(uint256 => string) public latestResponses;

    function getLatestPrompt() external view returns (string memory) {
        return latestPrompts[modelId];
    }

    function getLatestResponse() external view returns (string memory) {
        return latestResponses[modelId];
    }

    constructor(IAIOracle _aiOracle) AIOracleCallbackReceiver(_aiOracle) {
        callbackGasLimit[11] = 5_000_000; // Llama
    }

    function setCallbackGasLimit(uint64 gasLimit) external {
        callbackGasLimit[modelId] = gasLimit;
    }

    mapping(uint256 => mapping(string => string)) public prompts;

    function getAIResult(
        string calldata prompt
    ) external view returns (string memory) {
        return prompts[modelId][prompt];
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
        latestPrompts[request.modelId] = string(request.input);
        latestResponses[request.modelId] = string(output);
        emit promptsUpdated(
            requestId,
            request.modelId,
            string(request.input),
            string(output),
            callbackData
        );
    }

    function estimateFee() public view returns (uint256) {
        return aiOracle.estimateFee(modelId, callbackGasLimit[modelId]);
    }

    function calculateAIResult(string calldata prompt) external payable {
        bytes memory input = bytes(prompt);
        bytes memory callbackData = bytes("");
        address callbackAddress = address(this);
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
