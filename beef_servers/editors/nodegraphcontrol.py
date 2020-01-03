"""***********************************************
* @brief
*  Base NodeGraph 
*
***********************************************"""
import wx;
import copy;
import math;
from edgesignal import EdgeSignal;
from nodecontrol import NodeControl, NodeMouseEvent;
from nodegraph import NodeGraph;
from nodewidget import NodeWidget;
import math;
from logger import Logger, LoggerLevel;
from logger import Logger as Log;
Logger.DebugMode  = True;
Logger.Level  = LoggerLevel.INFORMATION;

from nodeselectorcontrol import NodeSelectorControl;
from gridnodecontrol  import GridNodeControl;
from textnodecontrol import TextNodeControl;



class TestNodeWidget(NodeWidget):

     def __init__(self, text):
          super().__init__(text);
         
          self.SocketY   =  self.CreateInputSocket("Y");
          self.SocketX   =  self.CreateInputSocket("X");
          self.SocketZ   =  self.CreateInputSocket("Y");
          self.ResultXY  =  self.CreateOutputSocket("Result");
          for s in range(0,10):
              self.CreateOutputSocket("Result {0}".format(s));

          for s in range(0,10):
              self.CreateInputSocket("X {0}".format(s)); 
          self.Width  = 100;
          self.Height  = 100;

class GraphScene(NodeControl):
     __MAX_ZOOM_FACTOR  = 5;
     __MIN_ZOOM_FACTOR  = 1;
     __ZOOM_FACTOR      = 0.2;
     
     def __init__(self, widget = None):
          super().__init__("Scene");
          self.__ZoomFactor    =  1;
          self.__ScaleFactor   =  1;
          self.__AllowZooming  = False;
          self.BackColor       = wx.Colour("#00000000");
          self.BorderColor     = wx.Colour("#00000000");
          self.__Widget   = widget;

     @property
     def Widget(self):
          return self.__Widget;

     @property
     def AllowZooming(self):
          return self.__AllowZooming;

     @AllowZooming.setter
     def AllowZooming(self, status):
          if(type(status)  == bool):
               self.__AllowZooming  =  status;
     @property
     def ZoomFactor(self):
          return self.__ZoomFactor;
     
     # Use this value to scale the graph
     @ZoomFactor.setter
     def ZoomFactor(self, value):
          if( (type(value)  == int)):
               self.__ZoomFactor  =  value;
          elif(type(value) == float):
               self.__ZoomFactor  =  value;
          else:
               raise TypeError("@Zooming value must be a  number");

     @property
     def ScaleFactor(self):
          return self.__ScaleFactor;

     @ScaleFactor.setter
     def ScaleFactor(self, value):
          allow  = False;
          if(type(value)  == int):
               allow  = True;
          if(type(value) == float):
               allow  = True;
          if(allow):
               self.__ScaleFactor =  value;
               
     def OnDraw(self,context, rect):
          super().OnDraw(context, rect);
          pass;
     
     @property
     def CanZoom(self):
          withinMin  = (self.ScaleFactor >= self.__MIN_ZOOM_FACTOR) ;
          withinMax  = (self.ScaleFactor <= self.__MAX_ZOOM_FACTOR);
          status  = (withinMin == True and withinMax == True);
          Logger.Debug("Scale Within Range Scale ={0} , status = {1}".format(self.ScaleFactor, status))
          return status

     def Zoom(self , zoomFactor , mousePosition):
          Logger.Debug("Zooming Scene");
          
          dxPosition      = mousePosition - self.Position
          xMousePosition  = dxPosition.x;
          yMousePosition  = dxPosition.y;
          #delta  =   event.GetWheelRotation() / dpi[0];
          wheel  =  1 if(zoomFactor > 0) else -1;
          self.ZoomFactor  =  math.exp(wheel * self.__ZOOM_FACTOR);
          
          if(self.CanZoom):
               traslateX  = (self.ScaleFactor * self.ZoomFactor);
               self.X  -=  ((yMousePosition / traslateX)  - (yMousePosition / self.ScaleFactor));
               self.Y  -=  ((xMousePosition / (traslateX))  - (xMousePosition / self.ScaleFactor));
              
               if(wheel == 1):
                    self.ScaleFactor  += self.ZoomFactor;
               else:
                    self.ScaleFactor  -= self.ZoomFactor;
                         
               Logger.Debug("xPos  =  {0}".format(-self.X));
               Logger.Debug("yPos  =  {0}".format(-self.Y));
               Logger.Debug("Zoom Factor  =  {0}%".format(self.ZoomFactor));
          else:
               if(self.ScaleFactor < self.__MIN_ZOOM_FACTOR):
                    if(wheel == 1):
                         self.ScaleFactor = 1;
               else:
                    if(self.ScaleFactor > self.__MAX_ZOOM_FACTOR):
                         if(wheel == -1):
                              self.ScaleFactor = self.__MAX_ZOOM_FACTOR;
          
          
     def AddNode(self, nodeControl):
          if(isinstance(nodeControl, NodeControl)):
               pass;
          
     def RemoveNode(self, nodeControl):
          if(isinstance(nodeControl, NodeControl)):
               pass;


     def RemoveEdge(self, edge):
          pass;

     def AddEdge(self,edge):
          pass;


     def EdgeCounts(self):
          return 0;


     def NodeCounts(self):
          return 0;


     def OnSelected(self , event):
          pass;

          
          



     

class LayoutManager(object):

     def DoLayout(self, graph):
          raise NotImplementedError("@DoLayout : must be implemented");


     
           
class NodeGraphControl(wx.Control):
     NODE_SCALE_FACTOR  =  100;
     GRID_SCALE_FACTOR  =  1;
     ZOOM_FACTOR        =  0.2;
     
     def __init__(self, parent):
        super().__init__(parent, id  = wx.ID_ANY);
        self.__UseBuffer    = True;
        self.__ReInitialBuffer = False;
        self.__Scene        = GraphScene(self);
        self.__Graph        = NodeGraph()
        self.Selector       = NodeSelectorControl(self.__Graph);
        self.__GridControl  = GridNodeControl(0,0);
        self.__GridControl.BackColor  = wx.Colour("#8c8c8c");
        self.__GridControl.ShowGrid  =  True;
        self.__GridControl.GridSize = 35;
        self.__GridControl.GridColor  =  wx.Colour("#00000017");
        self.LastPosition  = wx.Point(0,0);
        self.MoveGraph     = False;
        self.__mouseDown   = False;
        self.__Layout      = None;
        self.ScaleFactor   = 1;
        self.__ShowGrid    = True;
        self.__Buffer      = None;
        self.__Device      = None;
        self.__timer       = None;
        self.__Zoom        =  0;
        self.__MaxZoom     =  5;
        self.__MinZoom     =  1; # No scaling
        self.__ScrollAmount     = 0;
        self.__AccumulatedZoom  = 0;
        self.XOrigin  =  0;
        self.YOrigin  =  0;
        
        
        self.OnInitialUI();


     def Grid(self):
          return self.__GridControl;


     def OnInitialUI(self):
          self.SetDoubleBuffered(True);
          self.SetBackgroundColour("#404040");
          self.__timer      =  wx.Timer(self, wx.ID_ANY);
          self.Bind(wx.EVT_TIMER, self.OnTimer);
          self.__timer.Start(130)
          self.__InitGraphContext();
          self.HandleEvent();

     def __InitGraphContext(self):
        region =   wx.Rect(self.Position, self.Size)
        self.__Buffer    =  wx.Bitmap(region.Size);
       
        if(self.UseBuffer):
            self.__Device = self.__CreateDeviceContext(self.Buffer);
        else:
               self.__Device = wx.MemoryDC()
               self.__Device.SelectObject(self.__Buffer)
        
        
        self.Device.Translate(-self.XOrigin, -self.YOrigin);
        self.Device.Scale(self.ScaleFactor, self.ScaleFactor);
        Logger.Debug("GetDPI  = ({0},{0})".format(self.Device.GetDPI()));

        self.OnPaintBackground(self.__Device);
        self.RePaint();
        self.__ReInitialBuffer = False;



     def __CreateDeviceContext(self, buffer):
          device  =  None;
          
          if(type(buffer) == wx.Bitmap):
               native_device  =  wx.BufferedDC(None, self.__Buffer);
               device    = wx.GraphicsContext.Create(native_device);
               device.Clip(wx.Region(wx.Rect(wx.Point(0,0), buffer.Size)));
          return device;
          
        

     @property
     def Zoom(self):
          return self.__Zoom;
     
     # Use this value to scale the graph
     @Zoom.setter
     def Zoom(self, value):
          if( (type(value)  == int)):
               self.__Zoom  =  value;
          elif(type(value) == float):
               self.__Zoom  =  value;
          else:
               raise TypeError("@Zooming value must be a  number");

     @property
     def MinZoom(self):
          return self.__MinZoom;

     @property
     def MaxZoom(self):
          return self.__MaxZoom;
          
     @property
     def ShowGrid(self):
          return self.__ShowGrid;

     @ShowGrid.setter
     def ShowGrid(self, status):
          if(type(status) == bool):
               if(self.__ShowGrid != status):
                    self.__ShowGrid  = status;

     @property
     def CanRepaint(self):
          return self.__ReInitialBuffer;
    

     
     def OnTimer(self, event):
        if(self.CanRepaint):
            self.Invalidate();

     @property
     def Layout(self):
          return self.__Layout;

     @Layout.setter
     def Layout(self, layout):
          if(isinstance(layout, LayoutManager)):
               self.__Layout  =  layout;
            



     def OnPaintBackground(self, device):
          if(device != None):
               device.SetBrush(wx.Brush(self.GetBackgroundColour()));
               device.DrawRectangle(self.Position.x, self.Position.y, self.Size.Width, self.Size.Height);
               if(self.__GridControl != None):
                  self.__GridControl.Size  =  self.Size;
                  self.__GridControl.Draw(device);
        
     def Invalidate(self):
        self.__InitGraphContext();
        self.RePaint();
        self.Refresh ();
        
     @property
     def Device(self):
          return self.__Device;

     
     @property
     def Graph(self):
          return self.__Graph;
        
        
     def RePaint(self):
        if(self.__Device != None):
            bounds  = wx.Rect(self.Position, self.Size);
            self.__Device.Clip(wx.Region(bounds));
            self.Draw(self.__Device,bounds);
            

     def HandleEvent(self):
       if(self.Parent != None):
            self.Bind(wx.EVT_PAINT, self.OnPaint);
            self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown);
            self.Bind(wx.EVT_MOTION, self.OnMouseMove);
            self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp);
            self.Bind(wx.EVT_SIZE, self.OnResize);
            self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel);
            #self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave);
       pass;


     @property
     def CanZoom(self):
          withinMin  = (self.ScaleFactor >= self.MinZoom) ;
          withinMax  = (self.ScaleFactor <= self.MaxZoom);
          status  = (withinMin == True and withinMax == True);
          Logger.Debug("Scale Within Range Scale ={0} , status = {1}".format(self.ScaleFactor, status))
          return status

     def OnMouseWheel(self,event):
          
          position = event.GetPosition();
          dpi  =  self.Device.GetDPI()
          Logger.Debug("Mouse Position{0}".format(position))

          if(event.ControlDown()):
                Logger.Debug("Control Down");
                dxPosition      = event.GetPosition() - self.Position
                xMousePosition  = dxPosition.x;
                yMousePosition  = dxPosition.y;
                delta  =   event.GetWheelRotation() / dpi[0];
                wheel  =  1 if(delta > 0) else -1;
                self.Zoom  =  math.exp(wheel * self.ZOOM_FACTOR);
                
                if(self.CanZoom):
                    traslateX  = (self.ScaleFactor * self.Zoom);
                    xPosition = 0;
                    yPosition = 0;
                    
                    
                    yPosition  =  ((yMousePosition / traslateX)  - (yMousePosition / self.ScaleFactor));
                    xPosition  =  ((xMousePosition / (traslateX))  - (xMousePosition / self.ScaleFactor));
                    self.XOrigin  -=  xPosition
                    self.YOrigin  -=  yPosition
                   
                    if(wheel == 1):
                         self.ScaleFactor  += self.Zoom;
                    else:
                         self.ScaleFactor  -= self.Zoom;
                         
                         
                    Logger.Debug("xPos  =  {0}".format(-self.XOrigin));
                    Logger.Debug("yPos  =  {0}".format(-self.YOrigin));
                    Logger.Debug("Zoom  =  {0}%".format(self.Zoom));
                else:
                    if(self.ScaleFactor < self.MinZoom):
                          if(wheel == 1):
                               self.ScaleFactor = 1;
                    else:
                         if(self.ScaleFactor > self.MaxZoom):
                              if(wheel == -1):
                                   self.ScaleFactor = self.MaxZoom;
                                   
                self.Invalidate();
                self.Update();
                event.Skip();
               
              
          elif (event.ShiftDown()):
               # Horizontal scrolling
               Log.Debug("Shift Down ");
               pass;
          else:
               # Vertical Scrolling
               pass;
          
          

     def OnMouseLeave(self, event):
         if(event != None):
              self.MoveGraph  = False;
              self.LastPosition  =  event.GetPosition();
              pass;
              self.__mouseDown = False;
              if(self.Selector != None):
                   self.Selector.Done();
         event.Skip();
              

     def Draw(self, dc, bounds):               
          if(self.Layout != None):
               self.Layout.DoLayout(self.Graph);
          self.__DrawNodes(dc, bounds);
          self.__DrawEdges(dc, bounds);
          
          if(self.Selector.CanSelect != False):
               #dc.BeginLayer(0.4)               
               self.Selector.Draw(dc);
               #dc.EndLayer();
          self.Redraw = False;
          


     def __DrawNodes(self, dc, bounds):
        try:
             for node in self.Graph.Nodes:
                 node.Draw(dc);
        except Exception  as err:
             raise ;

     def __DrawEdges(self, dc, bounds):
          for edge in self.Graph.Edges:
               edge.OnDraw(dc, bounds);


     def OnResize(self, event):
        self.__ReInitialBuffer  = True;


          
     @property
     def PositionOffset(self):
          return  (self.Position   - wx.Point(-self.XOrigin, self.YOrigin))
     
     def OnMouseUp(self, event):
        self.__mouseDown  = False;
        self.LastPosition  =  event.GetPosition() 
        position  = self.LastPosition + self.PositionOffset;
        
        self.Selector.HandleMouseUp(event);
        self.MoveGraph  = False;
        self.__ReInitialBuffer = True;            
        event.Skip();
        

     def OnMouseDown(self, event):
          if(event != None):
            self.LastPosition =  event.GetPosition();
            Logger.Debug("Mouse Down At {0}".format(self.LastPosition));
            button  = event.GetButton();
            if(button == wx.MOUSE_BTN_LEFT):
                 self.__mouseDown = True; 
                 if(event.ControlDown()):
                      self.MoveGraph  = True;
                      Logger.Debug("Move Graph");
                      pass;
                 else:
                     args  =  NodeMouseEvent(event.GetPosition(), 0);
                     self.Selector.HandleMouseDown(event);
        
          
     def OnMouseMove(self, event):
          if(self.__mouseDown):
               position  =  event.GetPosition() ;
               if(self.MoveGraph):
                    xDelta  =  position.x  - self.LastPosition.x;
                    yDelta  =  position.y  - self.LastPosition.y;
                    self.XOrigin -= xDelta;
                    self.YOrigin -= yDelta;
               else:
                    self.Selector.HandleMouseMove(event);
               self.LastPosition  = position ;
               self.Invalidate();
               self.Update();
               event.Skip();
     @property
     def UseBuffer(self):
          return self.__UseBuffer;

     @UseBuffer.setter
     def UseBuffer(self, value):
          if(type(value) == bool):
               self.__UseBuffer  = value;
        
     def OnPaint(self, event):
        if(self.UseBuffer):
             wx.BufferedPaintDC(self, self.Buffer);
        else:
             dc = wx.PaintDC(self)
             dc.DrawBitmap(self.Buffer, 0, 0);
        event.Skip();
      

     def CreateNode(self, point, size):
          node  =  self.Graph.CreateNode("Untitle");
          if(node != None):
               node.Size =  size;
               node.Position =  point;
          return node;

     @property
     def Buffer(self):
          return self.__Buffer;
     
     def CreateEdge(self, source, dest):
          edge  =  None;
          if(isinstance(source, NodeControl)):
               if(isinstance(dest, NodeControl)):
                   edge =  self.Graph.CreateEdge("", source, dest);
          return edge;


def  DemoStart():
   app = wx.App();
   frame = wx.Frame(None, id= wx.ID_ANY, size  =  wx.Size(500,500));
   graph = NodeGraphControl(frame);
   nodeWidget  = TestNodeWidget("Actuator Controller 2");
   
   graph.Graph.Nodes.append(nodeWidget);
   

   nodeControler  = NodeWidget("Actuator Controller");
   graph.Graph.Nodes.append(nodeControler);
   
   textNode =  NodeWidget("Signal Generator 1");
   graph.Graph.Nodes.append(textNode);

   textNode1 =  NodeWidget("Actuator Controller 2");
   graph.Graph.Nodes.append(textNode1);
   
   node  =  NodeControl("Actuator Controller");
   node.Size = wx.Size(100,100);
   node.BackColor = wx.Colour("#090876");
   node.BorderRadius = 100;
   graph.Graph.Nodes.append(node);
 
   node1 =  graph.CreateNode(wx.Point(10, 80), wx.Size(78,100));
   node1.BackColor = wx.Colour("#00FF00");
   graph.CreateNode(wx.Point(10, 70), wx.Size(100, 100));
   graph.Size  = frame.Size;
   
   frame.Show();
   app.MainLoop()       

if(__name__ == "__main__"):
   DemoStart()
   pass;
     


    
