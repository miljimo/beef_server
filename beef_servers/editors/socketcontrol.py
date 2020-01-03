import math;
import wx;
from logger  import Logger as Log;
from nodecontrol import NodeControl;


class SocketType(int):
     IN  = 0x01;
     OUT = 0x02;

class SocketDataModel:

     def __init__(self):
          pass;
     

class SocketControl(NodeControl):
     DEFAULT_HEIGHT  = 10;
     DEFAULT_WIDTH   = 10;

     def __init__(self, **kwargs):
          text       =  kwargs['text'] if ('text' in kwargs) else "";
          self.__SocketType  =  kwargs['socket_type'] if ('socket_type' in kwargs) else SocketType.IN;
          super().__init__(text);
          self.__IsMouseOver  = False;
          self.Width   = self.DEFAULT_WIDTH;
          self.Height  = self.DEFAULT_HEIGHT
          self.BackColor    =  wx.Colour("#4d4d4d");
          self.BorderColor  =  wx.Colour("#e6e6e6");
        
          self.BorderWidth  = 1;
          #Event that signal have to subscribed to when a value of the socket changed.
          self.ValueChanged   = None;

     def OnCalculatePreferrableSize(self, context):
          return wx.Size(self.DEFAULT_WIDTH, self.DEFAULT_WIDTH);
     

     @property
     def Type(self):
          return self.__SocketType;

     @Type.setter
     def Type(self, value):
          if(type(value) == int):
               self.__SocketInput  =  value;
               
     
     def OnDraw(self, context):
          if(context != None):
               context.SetPen(wx.Pen(self.BorderColor,self.BorderWidth));
               context.SetBrush(wx.Brush(self.BackColor));
               circlePath  =  context.CreatePath();
               position    =  self.Position;
               circlePath.AddEllipse(self.X, self.Y, self.Width, self.Height);
               context.DrawPath(circlePath);
              
