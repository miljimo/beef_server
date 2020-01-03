import wx;
import copy;
from namedobject import NamedObject;
import uuid;
from logger import Logger;
from events import Event;

class MouseButtons(int):
     INVALID       = 0x10;
     LEFT_BUTTON   = 0x00;
     RIGHT_BUTTON  = 0x01;
     MIDDLE_BUTTON = 0x02;
     
MOUSE_BUTTON_EVENT  = 0x012;

class NodeMouseEvent(Event):

     def __init__(self, position , button  = MouseButtons.INVALID ):
          super().__init__(MOUSE_BUTTON_EVENT);
          self.__Position  =  position;
          self.__Button    =  button;
          
     @property
     def Position(self):
          return copy.copy(self.__Position);
     @property
     def Button(self):
          return copy.copy(self.__Button);

class NodeControl(NamedObject):
     __ID_COUNTER  = 0;
     def __init__(self, name):
        super().__init__(name);
        self.__position     =  wx.Point(1,1);
        self.__backColor    =  wx.Colour("#999999");
        self.__BorderColor  =  wx.Colour("000000");
        self.__borderWidth  =  1;
        self.__size         = wx.Size(40,10);
        self.__id  = "{0}{1}".format(uuid.uuid4(), self.__ID_COUNTER);
        self.__ID_COUNTER = self.__ID_COUNTER + 1;
        self.__Selected  = False;
        self.__SelectedBorderColor  =  wx.Colour("#FF0000");
        self.__borderRadius  = 5;
        self.__IsDraggable   = False;
        self.__IsMouseDown   = False;
        self.__lastMousePosition =  wx.Point(0,0);

     @property
     def IsMouseDown(self):
          return self.__IsMouseDown;

     @IsMouseDown.setter
     def IsMouseDown(self, value):
          if(type(value)  == bool):
               self.__IsMouseDown =  value;
     

     @property
     def LastMousePosition(self):
          return self.__LastMousePosition;

     @LastMousePosition.setter
     def LastMousePosition(self, pos):
          if(type(pso) == wx.Point):
               self.__LastMousePosition  =  pos;
               

     @property
     def IsDraggable(self):
          return self.__IsDraggable;
     
     @IsDraggable.setter
     def IsDraggable(self, status):
          if(type(status)  == bool):
               self.__IsDraggable  = status;
               
               


     def OnMouseDown(self,mouseEvent ):
          if(isinstance(mouseEvent, NodeMouseEvent)):
               position =  mouseEvent.Position;
               if(position != None):
                    self.LastMousePosition = position;
                    self.IsMouseDown  =  True;
                    pass;
               pass;

     def OnMouseUp(self, mouseEvent):
          if(isinstance(mouseEvent, NodeMouseEvent)):
               self.LastMousePosition = mouseEvent.Position;
               self.IsMouseDown   = False;
               
              

     def OnMouseMove(self, mouseevent):
           if(isinstance(mouseEvent, NodeMouseEvent)):
               position = mouseEvent.Position;
               if(self.IsMouseDown):
                    if(self.IsDraggable):
                         delta  =  position - self.LastMousePosition;
                         self.Move(delta);
               self.LastMousePosition = position;


     def DragMove(self, position):
          
          pass;

     @property
     def BorderRadius(self):
          return self.__borderRadius;

     @BorderRadius.setter
     def BorderRadius(self, radius):
          radius  = float(radius);
          if(radius != self.__borderRadius):
               self.__borderRadius  = copy.copy(radius);
          
        
     @property
     def BorderWidth(self):
          return self.__borderWidth;

     @BorderWidth.setter
     def BorderWidth(self, value):
          if(type(value) == int):
               self.__borderWidth  =  value;
     @property
     def X(self):
          return self.Position.x;
     
     @property
     def Y(self):
          return self.Position.y;


     def SetPosition(self,position):
          if(type(position) == wx.Point):
               self.__position =  copy.copy(position);

     def GetPosition(self):
          return self.__position;
 

     @property
     def Size(self):
         return self.__size;

     @Size.setter
     def Size(self, size):
          if(isinstance(size, wx.Size)):
               self.__size  = copy.copy(size);
     
     @property
     def ID(self):
          return self.__id;

     def DoLayout(self, context):
          Logger.Debug("@Implemented this function to be able to layout your control.");
          pass;
    
     @property
     def Position(self):
        return self.__position;

     @Position.setter
     def Position(self, value):
          if(isinstance(value, wx.Point)):
             if(value != None):
                  self.__position  =  copy.copy(value);

     @property
     def Bounds(self):
        rect = None;
        if(type(self.Position) == wx.Point):
             if(type(self.Size)  == wx.Size):
                rect = wx.Rect(self.Position, self.Size);
        if(rect == None):
             rect  = wx.Rect(wx.Point(0,0),wx.Size(0,0));
             Logger.Debug("Node Bounds Is empty: This should never happend");
             Logger.Debug("Position type {0}".format(type(self.Position.x)));
             Logger.Debug("Size type {0}".format(type(self.Size)));
        return rect;
            

    
     @X.setter
     def X(self, xValue):
          self.__position.x  = copy.copy(xValue);

     @Y.setter
     def Y(self, yValue):
          self.__position.y  = copy.copy(yValue);


     @property
     def Width(self):
          return self.Size.Width;
     
     @Width.setter
     def Width(self, value):
          self.__size.Width  = copy.copy(value);


     @property
     def Height(self):
          return self.Size.Height;
     
     @Height.setter
     def Height(self, value):
          self.__size.Height  = copy.copy(value);
          


          
     @property
     def BackColor(self):
        return self.__backColor;
    
     @BackColor.setter
     def BackColor(self, value):
        if(isinstance(value, wx.Colour)):
            if(self.__backColor != value):
                self.__backColor  =  copy.copy(value);
                

     @property
     def BorderColor(self):
        return self.__BorderColor;
    
     @BorderColor.setter
     def BorderColor(self, value):
        if(isinstance(value, wx.Colour)):
            if(self.__BorderColor != value):           
                self.__BorderColor  =  copy.deepcopy(value);
               


     @property
     def Selected(self):
          return self.__Selected;

     @Selected.setter
     def Selected(self, value):
          if(value !=self.__Selected):
               self.__Selected = value;


     @property
     def SelectedBorderColor(self):
          return self.__SelectedBorderColor;

     @SelectedBorderColor.setter
     def SelectedBorderColor(self, value):
          if(type(value)  == wx.Colour):
              self.__SelectedBorderColor = value;
          
               
     def OnCalculatePreferrableSize(self, context):
          return wx.Size(self.Width, self.Height);
     
          
        
     def Intersect(self, point):
        return self.Bounds.Contains(point);

     def Move(self, unit):
        if(isinstance(unit, wx.Point)):
             self.Position = wx.Point(self.Position.x + unit.x, self.Position.y + unit.y);


     def Draw(self, context):
          if(context != None):
               #Calculate the control client area for both children and itsself.
               size  =  self.OnCalculatePreferrableSize(context); 

               if(isinstance(size, wx.Size) != True):
                    raise TypeError("@Draw: extecting DoLayout to size wx.Size");
               self.Size   = size;
               self.DoLayout(context)
               self.OnDraw(context);
     """
       Draw the visual appearance of the Node Control.
     """
     def OnDraw(self, dc):
        if(dc != None):

           path  = dc.CreatePath();
           
           # if the Node Control is selected change the border settings and color;
           if(self.Selected):
              dc.SetPen(wx.Pen(self.SelectedBorderColor, self.BorderWidth + 2));
           else:
                dc.SetPen(wx.Pen(self.BorderColor, self.BorderWidth));
                
           dc.SetBrush(wx.Brush(self.BackColor, wx.SOLID))
           path.AddRoundedRectangle(self.X,self.Y, self.Size.Width, self.Size.Height, self.BorderRadius);
           dc.DrawPath(path);
