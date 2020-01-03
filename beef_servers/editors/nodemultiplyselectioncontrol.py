"""
 The moudle contains the class for handling multi and single selctions.

 @Author  - Obaro I. Johnson
"""
import wx;
from nodegraph   import NodeGraph;
from nodecontrol import NodeControl;
from logger      import Logger;
import copy;

      
class NodeSelectorControl(NodeControl):

  
     def __init__(self, graphNode =  None):
          super().__init__("Selector");
          self.BackColor    =  wx.Colour("#00000026");
          self.BorderColor  =  wx.Colour("#0000FFF1");
          self.__CanSelect =  False;
          self.__StartPosition =  wx.Point(0,0);
          self.__CanMoveSelections  =  False;
          self.__graphNode =  graphNode;
          self.__NodeLists          = list();
          self.__SelectedNode       = None;
          self.__SingleSelection    = False;
          self.__LastMousePosition  = wx.Point(0,0);

     @property
     def StartPosition(self):
          return self.__StartPosition;
     
     @StartPosition.setter
     def StartPosition(self, value):
          if(type(value) == wx.Point ):
               self.__StartPosition =  copy.deepcopy(value);


     def GetDirection(self,pos):
          result  = 0;
          if(pos.x < 0):
               result |= self.WEST;
          if(pos.y < 0):
               result =0;

          return result;


     @property
     def Graph(self):
          return self.__graphNode;
     
     @Graph.setter
     def Graph(self, value):
          if(isinstance(value, NodeGraph)):
               if(self.__graphNode != value):
                    self.__graphNode =  value;

     @property
     def CanSelect(self):
          return self.__CanSelect;

     @CanSelect.setter
     def CanSelect(self, value):
          if(type(value) == bool):
               self.__CanSelect  =  value;
               if(self.__CanSelect != False):
                    self.CanMoveSelections  =  False;
                    self.__SingleSelection  =  False;
              
     
     def UpdatePosition(self, position):
          if(type(position) == wx.Point):
               if(self.Graph == None):
                    raise ValueError("@UpdatePosition : Graph Node must be set on the selection object to manipulated");
               """
                   width :
                    increase width if delta.x is positive
                   x
                     decrease x by delta.x if delta.x is negative
                     and then
                    
               """
               if(self.StartPosition != None):
                    size     =  self.__DetermineSize(self.StartPosition, position);
                    self.Position = self.__DeterminePosition(self.StartPosition, position);
                    self.Size     = size;
                    self.SelectAllNodesBetweenBounds();
               else:
                    Logger.Assert(True, "Start Position Not Set");
               
     def __DeterminePosition(self, p1, p2):
          newPosition  =  copy.deepcopy(p1);
          if(p1.x > p2.x):
               newPosition.x  =  p2.x;
          if(p1.y > p2.y):
               newPosition.y  = p2.y;
          return newPosition;

     def __DetermineSize(self, p1, p2):
          return wx.Size(abs(p1.x-p2.x), abs(p1.y -p2.y))
     @property
     def CanMoveSelections(self):
          return self.__CanMoveSelections;

     @CanMoveSelections.setter
     def CanMoveSelections(self, value):
          if(type(value) == bool):
               if(self.__CanMoveSelections != value):
                    self.__CanMoveSelections =  value;
                    if(self.__CanMoveSelections):
                         self.CanSelect  = False;
                    else:
                         self.Done();

     def AddSelection(self, control):
          if(isinstance(control, NodeControl)):
               control.Selected  = True;
               self.__NodeLists.append(NodeControl);

               
     def StartDrag(self, node):
          self.CanMoveSelections  = True;
          self.__SelectedNode  =  node;
          self.__SingleSelection  = True;

     @property
     def HasSelections(self):
         return (len(self.__NodeLists) > 0)
     

     def MoveSelections(self, delta):
          if(self.CanMoveSelections):
               if(self.__SingleSelection):
                    if(self.__SelectedNode != None):
                         self.__SelectedNode.Move(delta);
               else:
                    
                  if(type(delta) == wx.Point):
                    self.Position  += delta;
                    for  node in self.__NodeLists:
                         node.Position +=delta;

     @property
     def IsSingleSelection(self):
          return self.__SingleSelection and self.CanSelect;


     def Done(self):
         self.CanMoveSelections  = False;
         self.CanSelect       = False;
         self.Size  = wx.Size(0,0);
         self.Position=  wx.Point(0,0);
         self.__StartPosition = wx.Point(0,0);
         self.UnSelectAll();
         self.__NodeLists.clear();
         self.__SingleSelection  = False;
         if(self.__SelectedNode != None):
              self.__SelectedNode.Selected  = False;
         self.__SelectedNode  = None;


     def UnSelectAll(self):
          for node in  self.__NodeLists:
            if(node.Selected == True):
                 node.Selected  = False;
          self.__NodeLists.clear();
               

     def SelectAllNodesBetweenBounds(self):
          self.UnSelectAll();
          bounds  = self.Bounds;
          for node in self.Graph.Nodes:
             if(bounds.Intersects(node.Bounds)):
                 node.Selected  = True;
                 self.__NodeLists.append(node);

     def __HintTestSelectedObject(self,pos):
          control = None;
          for  node in  self.__NodeLists:
               if(node.Selected):
                    if(node.Bounds.Contains(pos)):
                         control  = node;
                         break;
          return control;

     def GetNodeByPosition(self, pos):
          selectedNode  = None;

          for node in self.Graph.Nodes:
               if(node.Bounds.Contains(pos)):
                    selectedNode = node;
                    break;

          return selectedNode;

     def HandleMouseUp(self, event):
             """
               If The Move is drop within do not un select yet.
               
             """
             self.__LastMousePosition  = event.GetPosition();
             if(self.HasSelections != True):
                  self.Done();
             if(self.IsSingleSelection):
                  if(self.CanSelect == False):
                       self.Done();
                       Logger.Debug("@Selector Handle Mouse Up: Single Selection Completed , CanSelect {0}".format(self.CanSelect));
                  
             elif(self.Bounds.Contains(event.GetPosition()) != True):
                  if(self.CanMoveSelections):
                       self.CanMoveSelections  =  False;
                       self.UnSelectAll();
                       
             if(self.HasSelections):          
                  if(self.CanSelect):
                       self.CanMoveSelections = True;

     def HandleMouseDown(self, event):
          if(event.GetButton() == wx.MOUSE_BTN_LEFT):
               self.__LastMousePosition = event.GetPosition();
               
               if(self.CanMoveSelections == False):
                    Logger.Debug("@Logger: Left Mouse Down On CanMoveSelection False");
                    self.__HandleMouseSelection(event);
                               
               else:
                    self.CanMoveSelections  =  True;
                    self.HintTest(event.GetPosition());
                    
                    if(self.Hint != True):
                         self.Done();
                         self.__HandleMouseSelection(event);

     def HandleMouseMove(self, event):
          currentPosition =  event.GetPosition();
          delta  = currentPosition  -  self.__LastMousePosition;
          
          if(self.CanMoveSelections != True):
                   if(self.CanSelect  == True):
                        self.UpdatePosition(currentPosition);
          else:
               if(self.CanMoveSelections):
                         
                         """
                             Move the group of selected elements
                             this element should be part of the  Node Control
                             NodeSelectorControl
                         """
                         if(self.Hint):
                              self.MoveSelections(delta);
                         else:
                              self.UnSelectAll();
                              self.CanMoveSelection = False;
                              self.CanSelect        = False;
          
          self.__LastMousePosition  = currentPosition;                              
                               
     def __HandleMouseSelection(self, event):
          if(self.CanSelect != True):
               pos =  event.GetPosition();
               selectedControl  = self.GetNodeByPosition(pos);
               if(selectedControl != None):
                    Logger.Debug("@Logger: Start dragging selections");
                    self.AddSelection(selectedControl);
                    self.StartDrag(selectedControl);
               else:
                   self.StartPosition  =  pos;
                   self.CanSelect      =  True;

     
     def HintTest(self,pos):
          self.__SelectedNode    = self.__HintTestSelectedObject(pos);
          if(self.__SelectedNode != None):
               self.Graph.UpdateTopMostNode(self.__SelectedNode);
          return self.__SelectedNode;


     @property
     def Hint(self):
          return (self.__SelectedNode != None);
