import wx;
from edgesignal import EdgeSignal as Edge;
from nodecontrol import NodeControl ;



class NodeGraph(object):

     def __init__(self):
          self.__nodes  =  list();
          self.__edges  =  list();
          
     def CreateNodeIfNotExists(self , name):

        node  = self.GetNodeByName(name);
        exists = (node != None);
        if(exists != True):
          node =  self.CreateNode(name);
        return node;

     def CreateEdgeIfNodeExists(self, name):

        edge   =  self.GetEdgeByName(name);
        exists = (edge != None);
        
        if(exists != True):
            edge  = Edge(name);
            self.Edges.append(edge);

        return edge;

     
     def CreateEdge(self, name, source, dest):
          edge   =  self.CreateEdgeIfNodeExists(name);
          edge.Source  =  source;
          edge.Destination =  dest;

          return edge;


     def GetNodeByName(self, name):
        node = None;
        
        if(name in self.__nodes):
            node  = self.nodes[name];

        return node;

     def GetEdgeByName(self, name):
        edgeResult  = None;
        
        for edge in self.__edges:
            if(edge.Name  == name):
                edgeResult  = edge;
                break;
        return edgeResult;
        
     @property
     def Nodes(self):
        return self.__nodes;

     @property
     def Edges(self):
        return self.__edges;


     def Connect(self,s, d):
         edge = None;
         s     = s  if(isinstance(s, NodeControl)) else None;
         d     = d  if(isinstance(d, NodeControl)) else None;
         
         if( (s != None)  and (d != None)):
             edge  = self.GetEdgeBetween(s, d);
             
             if(edge == None):
                 edge = Edge(s.Name, s, d);
                 self.__edges.append(edge);
                 print(edge.Destination)
                 print(edge.Source);
             else:           
                 edge.Connect(s, d);
         
         return edge;
    

     def GetEdgeBetween(self, source, dest):
        edgeResult  = None;

        for edge in self.__edges:
            
            if(((edge.Source == source) or (edge.Source  == dest)) or
               ((edge.Destination == source) or (edge.Destination == dest))):
                edgeResult = edge;
                break;

        return edgeResult;

     def UpdateTopMostNode(self, node):
          if(isinstance(node, NodeControl)):
               self.Nodes.remove(node);
               self.Nodes.append(node);


     def TrySelectNodeByPosition(self, position):
          node = None;
          
          if(type(position) == wx.Point):
               node  =  self.GetNodeByPosition(position);
               if(node != None):
                    self.UpdateTopMostNode(node);
                    
          return node;
               


     def CreateNode(self, nodeName):
        node  = None;
        
        if(type(nodeName) == str):
            node  = NodeControl(nodeName);
            self.Nodes.append(node);
        return node;

     
                    
     
     def GetNodeByPosition(self, point):
        result = None;
        for node in self.__nodes:
            #print("Is Point {0} in  {1}".format(point, node.Bounds))
            if(node.Intersect(point)):
                result  = node;
                break;
        return result
     
     def __str__(self):
       value =  "{0} :{1}".format(self.Name, self.Nodes);
       for node in self.Nodes:
            "{0}".format(node);
       return value;

     
if (__name__ == "__main__"):
      graph  = NodeGraph();
      
