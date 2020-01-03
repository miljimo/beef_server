
"""
@Description

  The module is a set of classes for the property event implementations.
  
"""

from   namedobject  import NamedObject;
from   logger       import Logger;


class Event(object):

    def __init__(self, typeid ):
        self.__typeid  = typeid;
        self.__stopPropagation = False;

    @property
    def Type(self):
        return self.__typeid;

    @property
    def StopPropagation(self):
        return self.__stopPropagation;

    @StopPropagation.setter
    def StopPropagation(self, stopStatus):
        if(type(stopStatus)  == bool):
            self.__stopPropagation = stopStatus;


class Subscriber(object):

    def __init__(self):
        pass;

    def __call__(self, event):
        if(isinstance(event, Event) != True):
             raise ValueError("@Subscriber: event must be an object of event type");
        self.OnNotify(event);


    def OnNotify(self,  event):
        raise NotImplementedError("@Subscriber- OnNotify must be implement");


class Publisher(NamedObject):

    def __init__(self, name):
        NamedObject.__init__(self, name);
        self.__subscribers = list();

    def Publish(self ,event):
        nitems =   0;
        
        if(isinstance(event , Event)):
            for sub in self.__subscribers:
                if(sub != None):
                    if(event.StopPropagation == True):
                        break;
                    sub(event);
                    nitems = nitems + 1;
        return nitems;


    def Subscribe(self, callableObj):
        status  = False;
        
        if(callable(callableObj) != True):
            raise ValueError("@Subscriber->Subscribe: parameter 1 must be a callable object or type of Subscriber");

        if(self.__Exists(callableObj) != True):
            self.__subscribers.append(callableObj);
            status  = True;
            
        return status;

    def UnSubscribe(self,callableObj):
          status = False;
          for sub in self.__subscribers:
              if(sub == callableObj):
                  self.__subscribers.remove(callableObj);
                  status  = True;
                  break;
                
          return status;

    def __Exists(self , callableObj):
        status  = False;
        
        if(callable( callableObj)):
            for sub in self.__subscribers:
                if(sub  == callableObj):
                    status  = True;
                    break;

        return status;
        


    def __call__(self, event):
        return self.Publish(event);


    def __del__(self):
        self.__subscribers = None;


class EventHandler(object):
    def __init__(self, name):
        self.__publisher = Publisher(name);

    @property
    def Logger(self):
        return Logger;
    
    def __call__(self, event):
        if(isinstance(event, Event)):
           ncounts =  self.__publisher.Publish(event);

    def __iadd__(self, other):
        if(callable(other)):
            self.__publisher.Subscribe(other);
        return self;
    
    def __isub__(self, other):
        if(callable(other)):
            self.__publish.UnSubscribe(other);
        return self;
    


class BindingProperty(object):

    def __init__(self, obj, propertyName):
        if(hasattr(obj, propertyName) != True):
            raise ValueError("@BindingSource: object does not have property {0}".format(proeprtyName));
        if( (type(obj) == dict) or (type(obj) == list) or (type(obj) == tuple)):
            raise ValueError("@BindingSource: object must not be a list, tuple or dictionary");
        
        self.__Source              = obj;
        self.__PropertyName        = propertyName;

    @property
    def PropertyName(self):
        return self.__PropertyName;

    @property
    def Source(self):
        return self.__Source;

    @property
    def Value(self):
        return getattr(self.Source, self.PropertyName);

    @Value.setter
    def Value(self, value):
        if(value != self.Value):
            setattr(self.Source, self.PropertyName, value);

 
        

class BindingPropertyEvent(Event):

    def __init__(self, source, propertyName):
        Event.__init__(self, "{0}->{1}".format(type(source), propertyName));
        if(hasattr(source, propertyName) and (type(propertyName) == str)):
            self.__Source          =  source;
            self.__propertyName    =  propertyName
            
        else:
            raise ValueError("@PropertyEvent: Invalid  parameters ");

    @property
    def Value(self):
        return getattr(self.Source, self.PropertyName);

    @property
    def PropertyName(self):
        return self.__propertyName;

    @property
    def Source(self):
        return self.__Source;
    
class BindingType:
    ONE_WAY = 0x01;  # From source to destination only
    TWO_WAY = 0x02;  #  From source to destination and from destination to source.



class Binding(Subscriber):

    def __init__(self, source ,dest , mode  = BindingType.ONE_WAY):
        if(isinstance(source, BindingProperty) != True):
            raise ValueError("@BindingProperty: object must be an instance of PropertySource");
                             
        if(isinstance(dest, BindingProperty) != True):
            raise ValueError("@BindingProperty: object must be an instance of PropertySource");
        
        self.__sourceProperty = source;
        self.__destProperty   = dest;
        self.__mode           =  mode;
       

    @property
    def Mode(self):
         return self.__mode;


    @Mode.setter
    def Mode(self, value):
        if(type(value)  == int):
            self.__mode = value;
            

    @property
    def SourceProperty(self):
        return self.__sourceProperty;

    @property
    def DestinationProperty(self):
        return self.__destProperty;
        
                             

    def OnNotify(self, event):
        # One-way binding
        if(isinstance(event,BindingPropertyEvent) != True) :
             Logger.Except("@OnNotify: event object must be an instance of PropertyBindingEvent");
           
        if(event.Source ==  self.SourceProperty.Source):
             if(self.DestinationProperty.Value != event.Value):
                 self.DestinationProperty.Value  = event.Value;
             
             
        if ( (event.Source  == self.DestinationProperty.Source)
             and (self.Mode  == BindingType.TWO_WAY)):
            if(self.SourceProperty.Value !=  event.Value):
                self.SourceProperty.Value  = event.Value;
          

"""
 The property changed handler handles
 
"""
        
class PropertyChangedHandler(EventHandler):

    def __init__(self):
        EventHandler.__init__(self, "PropertyChanged");
        

    def __call__(self, source, propertyname):
        if(hasattr(source, propertyname)):
           event  =  BindingPropertyEvent(source, propertyname);
           EventHandler.__call__(self, event);


    def __iadd__(self, other):
        clsSelf  = self;
        if(callable(other)):
            if(isinstance(other, Binding) != True):
               Logger.Except("@PropertyChangedEvent : parameter 1 must be an instance of BindingProperty");
                 
            clsSelf =  EventHandler.__iadd__(self, other);
            
        return clsSelf;

    
class PropertyNotifyChanged(object):

    def __init__(self):
        self.PropertyChanged = PropertyChangedHandler();
        pass;

    def Bind(self, propertyname, destProperty  , mode = BindingType.TWO_WAY):

        if(isinstance(destProperty, BindingProperty)):
            binding  =  Binding(BindingProperty(self, propertyname), destProperty, mode);

            self.PropertyChanged += binding;
            if(mode  == BindingType.TWO_WAY):
                if(isinstance(binding.DestinationProperty.Source,PropertyNotifyChanged)):
                    binding.DestinationProperty.Source.PropertyChanged +=  binding;



    def RaisePropertyChanged(self, name):
        if(self.PropertyChanged != None):
            self.PropertyChanged(self, name);
                    
            
"""
Testing the class to make sure it does what its support to do.
"""
if __name__ == '__main__':
    class TestSubscriber(Subscriber):

           def OnNotify(self, event):
               print(event.Type);

               
    def TestEvent():
       print("Testing Event Object");
       event =  Event(8);
       print(event.Type);
       print(event.StopPropagation);
       event.StopPropagation =  True;
       print(event.StopPropagation);
       
    def SubscriberTest():

       try:
           sub  =  TestSubscriber();
           sub(Event("event.callable"));
       except Exception as e:
           print (e);


    def  TestPublisher():
        publisher  =  Publisher("Publisher");
        s =  TestSubscriber();
        
        publisher.Subscribe(s);
        publisher.Publish(Event("publisher.event.test"));
        publisher.UnSubscribe(s);
        publisher.Publish(Event("publisher.event.test"));


    def TestBindingSource():#Testing classes;
    
        class Signal(PropertyNotifyChanged):

              def __init__(self):
                  PropertyNotifyChanged.__init__(self);
                  self.__name  = "";

              @property
              def Name(self):
                  return self.__name;

              @Name.setter
              def Name(self, value):
                  self.__name = value;
                  self.RaisePropertyChanged("Name");
              
         
        class ModeSwitch(PropertyNotifyChanged):

            def __init__(self):
                PropertyNotifyChanged.__init__(self);
                self.__DisplayName = "";
                pass;

            @property
            def DisplayName(self):
                return self.__DisplayName;
            
            @DisplayName.setter
            def DisplayName(self, value):
                self.__DisplayName  = value;
                self.RaisePropertyChanged("DisplayName");

        class ValuerLinearise(object):


            def __init__(self):
               self.__Type ="";
               
            @property
            def Type(self):
               return self.__Type;

            @Type.setter
            def Type(self, value):
                print("Value  -  {0}".format(value));
                self.__Type  = value;


        s = Signal();
        m = ModeSwitch();
        t=  ValuerLinearise();
        
        m.Bind("DisplayName", BindingProperty(s, "Name"), BindingType.TWO_WAY);
        s.Bind("Name", BindingProperty(t, "Type"));
        m.DisplayName  = "Johnson";
        print(s.Name);
        m.DisplayName         = "Love";

        print(s.Name);
     
        
    TestPublisher();   
    SubscriberTest();
    #Test event object
    TestEvent();
    TestBindingSource();
   
   

            
