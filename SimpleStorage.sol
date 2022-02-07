// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.6.0;

contract SimpleStorage {
    // this will get initialized to 0!
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function set(uint256 newFavoriteNumber) public {
        favoriteNumber = newFavoriteNumber;
    }

    function get() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory personName, uint256 personFavoriteNumber)
        public
    {
        people.push(People(personFavoriteNumber, personName));
        nameToFavoriteNumber[personName] = personFavoriteNumber;
    }
}
