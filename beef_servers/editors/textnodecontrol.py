import wx;
from nodecontrol import NodeControl;
from logger import Logger;


class TextNodeControl(NodeControl):
     DEFAULT_FONT_SIZE  =  10;
     def __init__(self, text, font  = None):
          super().__init__(text);
          self.__Text      = text if(type(text)  == str) else self.throw_error("expecting a text to be string");
          self.__TextFont  =  font;
          self.__TextColor = wx.Colour("#FFFFFF");
          self.__TextPosition  =  self.Position;
          self.BackColor  = wx.Colour("#FFFFFF00");
          self.BorderRadius  = 0;
          self.__textHeight =  0;
          self.__textWidth  =  0;

     @property
     def TextColor(self):
          return self.__TextColor;

     @TextColor.setter
     def TextColor(self, value):
          if(type(value)  == wx.Colour):
               self.__TextColor  = value;

     @property
     def TextFont(self):
          if(self.__TextFont  == None):
               self.__TextFont  =  wx.Font(self.DEFAULT_FONT_SIZE , wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT, False);
               
          return self.__TextFont;

     @TextFont.setter
     def TextFont(self, value):
          if(type(value)  == wx.Font):
               self.__TextFont  = value;
               

     def throw_error(self, text):
          raise TypeError(text);

     
          
     @property
     def Text(self):
          return self.__Text;

     @Text.setter
     def Text(self, value):
          if(type(value) != str):
               raise TypeError("@Text: expecting it to be a string");


     def Draw(self, context):
     
       super().Draw(context);

     def OnCalculatePreferrableSize(self, context):
          self.__OnPreDrawUISettings(context);
          size  = wx.Size(self.Width,self.Height);
          PADDING  = 10;

          if(size != None):
               (width , height)  =  context.GetTextExtent(self.Text);
               size.Width  =  max(width +  PADDING,  size.Width);
               size.Height =  max(height + PADDING, size.Height) ;
               self.__textWidth  = width;
               self.__textHeight  = height;

          self.Size  =  size;
          return self.Size;
     """
        DoLayout:
        This allow the user to layout the control
        the way the wants.
     """
     def DoLayout(self, context):
          Logger.Debug("Text Width Size  =  {0}".format(self.Size.Width));
          Logger.Debug("Text Height Size  = {0}".format(self.Height));
          xPos =  self.X + (self.Width / 2) -   (self.__textWidth / 2);
          yPos =  self.Y + (self.Height /2)  -  (self.__textHeight / 2);
          self.__TextPosition = wx.Point(xPos, yPos);
          Logger.Debug("Text Position {0}".format(self.__TextPosition));
          

     def __OnPreDrawUISettings(self, context):
          gFont  =  context.CreateFont(self.TextFont, self.TextColor);
          if(gFont == None):
               raise ValueError("No Font find");
          context.SetFont(gFont);
          
         

     def OnDraw(self, context):
          Logger.Debug("Drawing Text");
          super().OnDraw(context);
          context.DrawText(self.Text, self.__TextPosition.x, self.__TextPosition.y)


