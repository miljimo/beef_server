import wx;
import math;
from nodecontrol import NodeControl;


class ContentControl(NodeControl):

     def __init__(self):
          super().__init__("Content");
          self.__Children =  list();
          

     @property
     def Children(self):
          return self.__Children;
          
