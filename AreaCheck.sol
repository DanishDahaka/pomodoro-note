// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.8.0;

/**
 * @title AreaCheck
 * @dev Allow for 
 */
contract AreaCheck {

    uint256[3] public areaSize = [100,200,300];
    bool[3] public areaTaken = [false,false,false];
    string[3] public supplierNames;
    string[3] public buyerNames;
    

    /**
     * @dev Check whether an area is taken or not
     * @param areaPosition for the forest inside areaSize
     * @return taken
     */
    function isBlocked(uint256 areaPosition) public view returns (bool taken) {
        
        taken = areaTaken[areaPosition];
        
        return taken;
        
    }
    
    /**
     * @dev Calculate the amount of carbon based on the area which is reserved
     * @param areaPosition for the forest inside areaSize
     * @return tokenAmount
     * @return supplierN
     * @return buyerN
     */
    function calcTokenAmount(
        uint256 areaPosition, 
        string memory supplierName,
        string memory buyerName
    ) 
        public returns (
        uint256 tokenAmount,
        string memory supplierN, 
        string memory buyerN
    ) 
    {
        
        bool blocked = isBlocked(areaPosition);
        
        require(blocked==false,"Area is taken");
        // 1 hectar equals 10 metric tons of carbon
        tokenAmount = 10 * areaSize[areaPosition]; 
        areaTaken[areaPosition] = true;
        
        
        
        //setting the names inside the supplier/buyer arrays
        supplierNames[areaPosition] = supplierName;
        buyerNames[areaPosition] = buyerName;
    
         
        return (tokenAmount, supplierName, buyerName);
        
    }
    
}