import wx;
import math;
from contentcontrol import ContentControl;
from socketcontrol import SocketControl,SocketType;


class SocketContent(ContentControl):
     __NODE_INPUT_TAG  = "Inputs";
     __NODE_OUTPUT_TAG = "Outputs";
     __HEIGHT_OFF_SET  = 5;
     
     def __init__(self):
          super().__init__();
          self.__sockets   = dict();
          self.__sockets[self.__NODE_INPUT_TAG]    = list();
          self.__sockets[self.__NODE_OUTPUT_TAG]   = list();

     @property
     def Inputs(self):
          return self.Sockets[self.__NODE_INPUT_TAG];

     @property
     def Outputs(self):
          return self.Sockets[self.__NODE_OUTPUT_TAG];

     @property     
     def Sockets(self):
          return self.__sockets;

     

     def AddSocket(self, socket):
          if(isinstance(socket, SocketControl)):
               if(socket.Type  == SocketType.IN):
                    if(self.__Exists(socket, self.Inputs) != True):
                         self.Inputs.append(socket);
               else:
                    if(self.__Exists(socket, self.Outputs) != True):
                         self.Outputs.append(socket);
                        


     def RemoveSocket(self, socket):
          if(isinstance(socket, SocketControl)):
               if(socket.Type == SockeType.IN):
                    for node in self.Inputs:
                         if ( (node  == socket) or (node.Name ==  socket.Name)):
                              self.Inputs.remove(node);
                              break;
               else:
                    for node in self.Outputs:
                         if((node == socket) or (node.Name  == socket.Name)):
                              self.Outputs.remove(node);
                              break

                       
     def __Exists(self, socket , sockets):
          status = False;
          if(socket  == None):
               return status;
          for node in sockets:
               if((node == socket) or (node.Name  == socket.Name)):
                    status =  True;
                    break;
               
          return status;


     def __DoLayoutInputSockets(self, context):
          yoffset   = self.Y  + self.Height - (SocketControl.DEFAULT_WIDTH + 10)
          xoffset   = self.X   - (SocketControl.DEFAULT_WIDTH / 2)
          
          for sock in self.Inputs:
               sock.Position =  wx.Point(xoffset, yoffset);
               sock.Size     =  sock.OnCalculatePreferrableSize(context);
               yoffset      -=  ((SocketControl.DEFAULT_WIDTH) + self.__HEIGHT_OFF_SET);

               if(yoffset <=0):
                    break;
               sock.DoLayout(context);
               pass;
           

     def __DoLayoutOutputSockets(self, context):
          yOffsetForOutputs  = self.Y   + SocketControl.DEFAULT_WIDTH  + 10;
          xOffsetForOuputs   = (self.X   +  (self.Width  - (SocketControl.DEFAULT_WIDTH / 2)));
          
          for sock in self.Outputs:
            sock.Position     = wx.Point(xOffsetForOuputs, yOffsetForOutputs);
            sock.Size         = sock.OnCalculatePreferrableSize(context);
            yOffsetForOutputs = sock.Y + sock.Height + self.__HEIGHT_OFF_SET;
            socketRect        =  sock.DoLayout(context);

     def __CalculateSocketSize(self):
          size    =  wx.Size(0,0);
          length  = len(self.Inputs);
          length_outputs  = len(self.Outputs);
          
          input_actual_height  =   (length * SocketControl.DEFAULT_WIDTH) + (length * self.__HEIGHT_OFF_SET) + 20;
          output_height        =   (length_outputs * SocketControl.DEFAULT_WIDTH) + (length_outputs * self.__HEIGHT_OFF_SET) + 20;
          
          size.Width   =  max(self.Width, SocketControl.DEFAULT_WIDTH);
          size.Height  =  max(input_actual_height, output_height);

          self.Size  = size;
          return size;


     def OnCalculatePreferrableSize(self, context):
          sockSize   = self.__CalculateSocketSize();
          return wx.Size(sockSize.Width, max(self.Height , sockSize.Height));
          
          
     
     def DoLayout(self, context):
          self.__DoLayoutInputSockets( context);
          self.__DoLayoutOutputSockets(context);
        
     def OnDraw(self, context):
          super().OnDraw(context);
          
          for socket in self.Inputs:
             socket.OnDraw(context);

          for socket in self.Outputs:
               socket.OnDraw(context);
         
          
