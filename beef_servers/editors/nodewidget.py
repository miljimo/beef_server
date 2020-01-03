import wx;
import math;
import copy;
from logger import Logger;
from logger import Logger as Log;
from nodecontrol import NodeControl;
from textnodecontrol import TextNodeControl;
from socketcontrol  import SocketControl,SocketType;
from contentcontrol import ContentControl;
from socketcontent  import SocketContent;
from titlepanelcontrol import TitlePanelControl;


class DataModel(object):

     def __init__(self):
          pass;

          
class NodeWidgetDataModel:

     def __init__(self):
          pass;


     def TriggerUpdate(self):
          
          pass;


class NodeWidthController:

     def __init__(self, view  , model):

          self.__widget    =  None;
          self.__dataModel =  None;
          #self.OnPropertyBinding();
          pass;

     
     
class NodeWidget(NodeControl):

     __DEFAULT_BORDER_RADIUS       = 2.5;
     
     def __init__(self, text ):
          super().__init__(text);
          self.BorderRadius         = 3;
          self.__Panel              =  TitlePanelControl(text);
          self.__Panel.Content      =  SocketContent();
          self.BackColor            =  wx.Colour ("#40404081");
          self.__Panel.BackColor    =  wx.Colour("#808080");
          self.__DataModel          =  None;
          self.SelectedBorderColor  =  wx.Colour("#ffcc0089");
          self.__Selected = False;

     def CreateInputSocket(self, text):
         socket =  None;
         if(isinstance(self.Panel.Content, SocketContent)):
              socket =  SocketControl(text = text, socket_type  = SocketType.IN);
              if(socket != None):
                   self.Panel.Content.AddSocket(socket);
         return socket;
                   
     def CreateOutputSocket(self, text):
          socket = None;
          
          if(isinstance(self.Panel.Content, SocketContent)):
               socket =  SocketControl(text = text, socket_type  = SocketType.OUT);
               if(socket != None):
                   self.Panel.Content.AddSocket(socket);
          return socket;

     @property
     def DataModel(self):
          return self.__DataModel;

   

     @DataModel.setter
     def DataModel(self, dataModel):
          if(isinstance(dataModel, IDataModel)):
               if(dataModel != self.__DataModel):
                    self.__DataModel = dataModel;
                    
     @property
     def Panel(self):
          return self.__Panel;

     @property
     def Header(self):
          return self.Panel.Header;


     def OnCalculatePreferrableSize(self, context):
          size  =  super().OnCalculatePreferrableSize(context);
          if(self.__Panel != None):
               panelSize  =  self.__Panel.OnCalculatePreferrableSize(context);
               self.__Panel.Size  = panelSize;
               size  = wx.Size(  max(self.Width , (panelSize.Width +self.BorderRadius) ),  max(self.Height , panelSize.Height + self.BorderRadius) );
               self.Size  = size;
          return size;
          
          
     @property
     def Selected(self):
         return self.__Selected;

     @Selected.setter
     def Selected(self, value):
         if(type(value)== bool):
            self.__Selected  = value;

     def DoLayout(self, context):
           xPos  =  self.X + ((self.Width/2) - (self.Panel.Width/2));
           yPos  =  self.Y +  (self.BorderRadius/2);
           self.Panel.Position   =  wx.Point(xPos,yPos);
           self.Panel.DoLayout(context);
           
           if(self.__DEFAULT_BORDER_RADIUS  != self.BorderRadius):
               self.BorderRadius = self.__DEFAULT_BORDER_RADIUS;
        

     def OnDraw(self, context):
          super().OnDraw(context);
          self.Panel.OnDraw(context);
          
          
          
