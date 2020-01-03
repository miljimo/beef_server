"""**************************************************************
* @Description
*   A name object
*
**************************************************************"""

class NamedObject(object):
    __UUID = 0;
    
    def __init__(self, name):
        self.__name  = name;
        self.__id    = self.__UUID + 1;
        
    @property
    def Name(self):
        return self.__name;

    @Name.setter
    def Name(self, value):

        if(type(value) != str):
             raise ValueError("Unexpected value provided");
        self.__name  = value;
        

    @property
    def ID(self):
        return self.__id;


if(__name__=='__main__'):

    nameObj  = NamedObject("testing_naming");
    print(nameObj.Name);
    nameObj.Name ="What is going on";
    print(nameObj.ID);
    
