// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "OAO/contracts/interfaces/IAIOracle.sol";
import "OAO/contracts/AIOracleCallbackReceiver.sol";

contract Summary is AIOracleCallbackReceiver {
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

    function summarizeProject(string calldata tokenName) external payable {
        string memory prompt = string.concat(
            "Summarize the following smart contract project for potential token buyers.\n",
            "Focus on key aspects such as tokenomics, security features, and unique selling points.\n",
            "Token name: ",
            tokenName
        );
        bytes memory input = bytes(prompt);
        address callbackAddress = address(this);
        bytes memory callbackData = bytes("");
        uint256 requestId = aiOracle.requestCallback{value: msg.value}(
            11, // Llama model ID
            input,
            callbackAddress,
            callbackGasLimit[11],
            callbackData
        );

        AIOracleRequest storage request = requests[requestId];
        request.input = input;
        request.sender = msg.sender;
        request.modelId = 11;
        emit promptRequest(requestId, msg.sender, 11, prompt);
    }

    struct Asset {
        string tokenName;
        string description;
        uint8 distribution;
    }

    function summarizeInvestment(Asset[4] memory assets) external payable {
        uint8 totalDistribution = 0;
        for (uint i = 0; i < 4; i++) {
            totalDistribution += assets[i].distribution;
        }
        require(totalDistribution == 100, "Distribution must total 100%");

        string memory prompt = string.concat(
            "Analyze and explain the following investment portfolio:\n\n",
            assetToString(assets[0], 1),
            assetToString(assets[1], 2),
            assetToString(assets[2], 3),
            assetToString(assets[3], 4),
            "\nPlease provide a comprehensive explanation of these assets and their distribution in the investment portfolio. ",
            "Consider the following points in your analysis:\n",
            "1. Brief description of each asset and its key characteristics\n",
            "2. Rationale behind the distribution percentages based on market cap\n",
            "3. Potential risks and benefits of this portfolio composition\n",
            "4. How this distribution might reflect current market trends or investor sentiment\n",
            "5. Any notable synergies or diversification benefits among the assets\n",
            "6. The significance of the specific tokens chosen for each asset category\n\n",
            "Provide your analysis in a clear, concise manner suitable for both novice and experienced investors."
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

    function assetToString(
        Asset memory asset,
        uint8 index
    ) internal pure returns (string memory) {
        return
            string(
                abi.encodePacked(
                    "Asset ",
                    uintToString(index),
                    ": ",
                    asset.description,
                    " (",
                    uintToString(asset.distribution),
                    "% of portfolio)\n",
                    "Token Name: ",
                    asset.tokenName,
                    "\n\n"
                )
            );
    }

    function uintToString(uint8 v) internal pure returns (string memory) {
        if (v == 0) return "0";
        uint8 digits = 0;
        uint8 x = v;
        while (x > 0) {
            digits++;
            x /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (v > 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + (v % 10)));
            v /= 10;
        }
        return string(buffer);
    }

    function addressToString(
        address _addr
    ) internal pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_addr)));
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(42);
        str[0] = "0";
        str[1] = "x";
        for (uint256 i = 0; i < 20; i++) {
            str[2 + i * 2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3 + i * 2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }
        return string(str);
    }
}
