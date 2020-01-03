import wx;
from namedobject import NamedObject;
from socketcontrol import SocketControl ;
from logger import Logger as Log;


class HasCreateConnection:

    def Connect(self, source, dest):
        raise NotImplementedError("@Connect: must be implemented error");
    
    
"""
 The edge signal         ---
 | |--------------------|   |
                         ---
"""
class EdgeSignal(NamedObject, HasCreateConnection):

    def __init__(self , name, sourceNode = None, destinationNode = None):
        super().__init__(name);
        self.__Source      = sourceNode if(isinstance(sourceNode, SocketControl)) else None;
        self.__Destination = destinationNode if(isinstance(destinationNode, SocketControl)) else None;
        self.__weight =  0.0;
        self.__path   = list();
        self.__Color = wx.Colour("#808080");

    @property
    def Color(self):
        return self.__Color;

    @Color.setter
    def Color(self, value):
        if(type(value) == wx.Colour):
            self.__Color  = value;

    @property
    def Source(self):
        return self.__Source;
    
    @Source.setter
    def Source(self , value):
         result  = value if(isinstance(value,SocketControl)) else None;
         if(result == None):
             raise TypeError("@Source: expecting a socket control ");
         self.__Source     = result;

    @property
    def Destination(self):
        return self.__Destination;
    
    @Destination.setter
    def Destination(self , value):
         result  = value if(isinstance(value,SocketControl)) else None;
         if(result == None):
             raise TypeError("@Destination: expecting a socket control ")
         self.__Destination     = result;

    @property
    def Weight(self):
        return self.__weight;

    @property
    def Connect(self, source, dest):
        connected  = False;
        if(isinstance(source,SocketControl) and isinstance(dest,SocketControl)):
             self.__sourceNode       = source;
             self.__destinationNode  = dest;
            
             connected  = True;
        return connected;

    @property
    def Path(self):
        if(len(self.__path)  ==  0):
             self.__path  =  list ();
             self.__path.append(self.Source.Position);
             self.__path.append(self.Destination.Position);            
        return self.__path;

    def Draw(self, context):
        pass;


    def OnDraw(self, dc, bounds):
        if(dc != None):
          
          if(self.Source != self.Destination):
              Log.Debug("From {0} to {1}".format(self.Source.Position, self.Destination.Position));
              path  = dc.CreatePath();
              dc.SetPen(wx.Pen(wx.Colour("#FFFFFF89"), 2));
              path.MoveToPoint(self.Source.X , self.Source.Y);
              path.AddLineToPoint(self.Destination.X, self.Destination.Y);
              dc.DrawPath(path);
                
       
    
