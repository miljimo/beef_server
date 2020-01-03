import wx;
from logger import Logger;
from  nodecontrol import NodeControl;

                 
                    

class GridNodeControl(NodeControl):

     DEFAULT_GRID_SIZE       = 10;
     DEFAULT_GRID_LENGTH     = 5;
     DEFAULT_GRID_LINE_WIDTH = 1;
     

     def __init__(self,width, height):
          super().__init__("GridControl");
          self.Width               = width if(type(width) == int) else 0;
          self.Height              = height   if(type(height) == int) else  0;
          self.__GridColor         = wx.Colour("#e6e6e612");
          self.__GridBoxLength     = self.DEFAULT_GRID_LENGTH;
          self.__GridSize          = self.DEFAULT_GRID_SIZE;
          self.__GridLineWidth     = self.DEFAULT_GRID_LINE_WIDTH;
          self.__ShowGrid          = False;
          self.Opacity             = 0.4;
          self.InitUI();

     @property
     def ShowGrid(self):
          return self.__ShowGrid;

     @ShowGrid.setter
     def ShowGrid(self, value):
          if(type(value)  == bool):
               self.__ShowGrid   = value;
          
     def InitUI(self):
          self.BackColor      = wx.Colour("#404040");
          pass;

     @property
     def GridSize(self):
          return self.__GridSize;


     @GridSize.setter
     def GridSize(self, value):
           self.__GridSize = value;

     @property
     def GridLineWidth(self):
          return self.__GridLineWidth;

     @GridLineWidth.setter
     def GridLineWidth(self, width):
          if (((type(width) == int) == True) or ((type(width) == float) == True)):
               self.__GridLineWidth  = width;

     @property
     def GridColor(self):
          return self.__GridColor;

     @GridColor.setter
     def GridColor(self, value):
          if(type(value) != wx.Colour):
               raise TypeError("@GridColor: must be of type wx.Colour");
          
          if(value != self.__GridColor):
               self.__GridColor  =  value;


     @property
     def GridBoxLength(self):
          return self.__GridBoxLength;

     @GridBoxLength.setter
     def GridBoxLength(self, value):
          if(type(value) == int):
               self.__GridBoxLength  = value;

               
     def __ComputeHorizontalPath(self, device , width , height):
            Logger.Debug("Computing the Horizontal grid Layout"); 
            path      = device.CreatePath();
            unitPath  = device.CreatePath();
            counter   =  0;
            yoffset =  self.GridSize;
            
            if(yoffset < 2):
                yoffset  = 2;
                self.GridSize = 2;
             
            while(yoffset  <= height):
                usePath  = path;
                
                if( (counter % self.GridBoxLength)  == 0):
                    usePath  = unitPath;
                    counter   = 0;
                    
                p1  = wx.Point(0, yoffset);
                p2  = wx.Point(width, yoffset);
                usePath.MoveToPoint(p1.x, p1.y);
                usePath.AddLineToPoint(p2.x, p2.y);
                yoffset = yoffset + self.GridSize;
                counter  =  counter + 1;

            Logger.Debug("Completed");

            return (path , unitPath);



     def __ComputeVerticalPath(self, device, width, height):
        Logger.Debug("Computing the vertical grid Layout"); 
        path      = device.CreatePath();
        unitPath  = device.CreatePath();
        counter   =  0;
        xoffset =  self.GridSize;
            
        if(xoffset < 2):
            xoffset  = 2;
            self.GridSize = 2;

        while( xoffset <= width):
                          
            if((counter % self.GridBoxLength) == 0):
                counter  =0;
                usePath  = unitPath;
            else:
                usePath           = path;
                               
            p1  = wx.Point(xoffset, 0);
            p2  = wx.Point(xoffset, height);
            usePath.MoveToPoint(p1.x, p1.y);
            usePath.AddLineToPoint(p2.x,p2.y);
            xoffset  = xoffset + self.GridSize;
            counter = counter + 1;
            
        Logger.Debug("Completed");
        return (path, unitPath);
         
     """
       Only override Draw when you know what you are doing 
     """
     def Draw(self, context):
          if(self.ShowGrid):
               super().Draw(context);

     def __DrawGrid(self, device):
               width   =  self.Size.Width;
               height  =  self.Size.Height;
               hPath,  hUnitPath      = self.__ComputeHorizontalPath(device, width, height);
                   
               vPath, vUnitPath  =  self.__ComputeVerticalPath(device, width, height);
                   
               hPath.AddPath(vPath);
               hUnitPath.AddPath(vUnitPath);
              
               device.SetPen(wx.Pen(self.GridColor, self.GridLineWidth));
               device.DrawPath(hPath);
               device.SetPen(wx.Pen(self.GridColor, self.GridLineWidth * 2));
               device.DrawPath(hUnitPath);
         


     def OnDraw(self, context):
          super().OnDraw(context);
          self.__DrawGrid(context);
          
          
