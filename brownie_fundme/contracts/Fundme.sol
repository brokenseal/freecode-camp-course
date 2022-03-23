// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeedInterface;

    constructor(address _priceFeedAddress) public {
        priceFeedInterface = AggregatorV3Interface(_priceFeedAddress);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized");
        _;
    }

    function fund() public payable {
        // 50 USD
        uint256 minimumFund = 50 * (10**18);

        require(
            getConversionRate(msg.value) >= minimumFund,
            "Minimum amount of 50 USD not reached"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        /*uint256 balance = getBalance();
        require(
            balance > 0,
            "Insufficient balance"
        );*/
        msg.sender.transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            addressToAmountFunded[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getVersion() public view returns (uint256) {
        return priceFeedInterface.version();
    }

    function getFundAmountForAddressInUsd(address patreon)
        public
        view
        returns (uint256)
    {
        return getConversionRate(addressToAmountFunded[patreon]) / 10**18;
    }

    function getPrice() public view returns (uint256) {
        // the returning price value shows as having 8 decimals
        // e.g. 2695 785 725 13
        (, int256 price, , , ) = priceFeedInterface.latestRoundData();
        uint8 weiDecimals = 18;
        uint256 decimalsDiff = weiDecimals - priceFeedInterface.decimals();

        // this math is there in order for the price in usd to have the
        // same amount of decimals as eth has
        // in reality no floating point numbers can be used, only integers
        // the decimal places are set at 10^18
        return uint256(price) * 10**(decimalsDiff);
    }

    function getConversionRate(uint256 ethAmountInWei)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmountInWei) / (10**18);

        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUsd = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;

        return (minimumUsd * precision) / price;
    }
}
