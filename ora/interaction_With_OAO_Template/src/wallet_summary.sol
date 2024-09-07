// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "OAO/contracts/interfaces/IAIOracle.sol";
import "OAO/contracts/AIOracleCallbackReceiver.sol";

contract WalletSummary is AIOracleCallbackReceiver {
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

        // Update latest prompt and response
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

    function summarizeInvestment(string calldata jsonData) external payable {
        string memory prompt = string.concat(
            "Here you have the crypto wallet protfolio of a user.\n\n",
            jsonData,
            "\n\nPlease provide a comprehensive explanation for the portfolio of the user.",
            "Consider the following points in your analysis:\n",
            "1. A simple description of all the assets the user has tokens\n",
            "2. A simple analysis of the user's investment strategy if his portfolio is diversified or not\n",
            "3. Potential risks and benefits if he has a diversified portfolio or not\n"
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
