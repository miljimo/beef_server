import wx;
import math;
import copy;
from logger import Logger;
from nodecontrol     import NodeControl;
from contentcontrol  import ContentControl;
from textnodecontrol import TextNodeControl;


class HeaderContent(NodeControl):


     def __init__(self , title  =  "untitle"):
          super().__init__(title);
          self.__TextControl = TextNodeControl(title);   
          

     def Title(self):
          return self.__TextControl.Text;
     

     def Title(self, text):
          if(type(text)  == str):
               self.__TextControl.Text  =  text;


     def OnCalculatePreferrableSize(self, context):
          result =  super().OnCalculatePreferrableSize(context);
          # Tell the TextControl to provides its preferable size
          textSize  =  self.__TextControl.OnCalculatePreferrableSize(context);
          width     =  max(textSize.Width, self.Size.Width);
          height    =  max(textSize.Height, self.Size.Height);
         
          result = wx.Size(width, height);
          if(result == None):
               raise ValueError("@OnCalculatePreferrableSize: result must be a size object");
          self.Size   = result;
          return result;


     def DoLayout(self, context):
          self.__TextControl.Position = self.Position;
          self.__TextControl.DoLayout(context);


     def OnDraw(self, context):
          self.__TextControl.OnDraw(context);
          
                         
        

class TitlePanelControl(NodeControl):

     CONTENT_HEIGHT = 150;
     CONTENT_WIDTH  = 100;

     def __init__(self, text):
          super().__init__(text);
          self.BackColour  = wx.Colour("#bfbfbf89");
          self.BorderColor = wx.Colour("#00000000");
          self.BorderWidth = 0;
          self.OnInitialUI(text);

     def OnInitialUI(self, text):
          self.BorderRadius  =  0;
          self.__header  = HeaderContent(text);
          
          if(self.__header != None):
               self.__header.Position     = self.Position;
               self.__header.BackColor    = wx.Colour("#bfbfbfF9");
               self.__header.BorderColor  = self.BorderColor;
         
          self.__Content   =  ContentControl();
          if(self.__Content != None):
            self.__InitContentStyle();
            

     def __InitContentStyle(self):
          if(self.Content != None):
               self.Content.Position      = self.Position ;
               self.Content.Width         = self.CONTENT_WIDTH;
               self.Content.Height        = self.CONTENT_HEIGHT;
               self.Content.BorderWidth   =  0;
               self.Content.BackColor     = wx.Colour("#FFFFFFF0");
               self.Content.BorderRadius  = 0;
               self.Content.BorderColor   = wx.Colour("#FFFFFF89");
               
               
     @property
     def Header(self):
          return self.__header;


     @property
     def Content(self):
          return self.__Content;
     
     @Content.setter
     def Content(self, content):
          if(isinstance(content, ContentControl)):
               if(content != self.__Content):
                    self.__Content  = content;
                    self.__InitContentStyle();


     def OnCalculatePreferrableSize(self, context):
          headerSize   =  self.Header.OnCalculatePreferrableSize(context);
          contentSize  =  self.Content.OnCalculatePreferrableSize(context);
          self.Content.Size  = contentSize;
          
          width                =  max(contentSize.Width, max(self.Width, headerSize.Width));
          height               =  max(self.Height, headerSize.Height + contentSize.Height);
          self.Header.Width    = width;
          self.Content.Width   = width;
          #Pack the content
          self.Width   =  width;
          self.Height  =  height;
          self.Size  =  wx.Size(width, height)
          return  self.Size;
                    

     def DoLayout(self, context):
          #Layout the Header
          self.Header.Position = copy.deepcopy(self.Position);
          self.Header.DoLayout(context);
          
          #Layout the content
          self.Content.Position  = wx.Point(self.Header.X,  self.Header.Y + self.Header.Height);
          self.Content.DoLayout(context);
          
          
         
     def OnDraw(self, context):
          super().OnDraw(context);
          self.Header.OnDraw(context);
          self.Content.OnDraw(context);
