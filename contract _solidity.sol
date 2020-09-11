pragma solidity ^0.6.10;

contract SimpleStorage {
    
    struct User {
        string uname ;
        uint256 index ; 
    } 
    struct Photo {
        string fig ;
       string time ; 
    } 
    uint256 workt =0;
    Photo[] photos;
    User[] users;
    bool c = false;
    uint256 x =0; 

    function setname (string memory _name ) public {
       users.push(User(_name , x++));
    }
    

    function checkname(string memory z) public  {
        
        for(uint i=0; i< users.length ;i++){
       if (keccak256(abi.encodePacked(users[i].uname)) == keccak256(abi.encodePacked(z))) {
              c =true;
              break;
        }else{c=false;}
        
        }
    }
    
    function comferm( ) public view returns (bool) {
        return c;
    }
     function deluser(string memory z) public  {
        
        for(uint i=0; i< users.length ;i++){
       if (keccak256(abi.encodePacked(users[i].uname)) == keccak256(abi.encodePacked(z))) {
            delete users[i];
            break;
        }
    }
    }
    // photos 
    function setphoto (string memory _fi ,string memory _time ) public {
       photos.push(Photo(_fi ,_time));
    }
    //
    function photoNumb ( ) public view returns (uint256) {
       return photos.length;
    }
    uint256 hash =0; 
     function getphoto1 (uint256 _x) public {
         _x=_x-1;
       if( _x < photos.length ){
           hash = _x;
       }
     }
    function getphoto2 ( ) public view returns (string memory) {
      
       return photos[hash].fig;
    }
    
     function getphototime ( ) public view returns (string memory) {
      
       return photos[hash].time;
    }
    
    
    // save work time 
    function addtime (uint256  _t) external {
        workt = workt + _t;
    }

    function getworkt ( ) public view returns (uint256) {
       return workt;
    }
    
}



pragma experimental ABIEncoderV2;

contract Test {

    string[] array;

    function push(string calldata _text) external {
        array.push(_text);
    }

    function get() external view returns(string[] memory) {
        return array;
    }
}
