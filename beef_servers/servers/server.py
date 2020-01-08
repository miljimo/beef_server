
import socket;
from threading import Thread, Lock;
import time;
import os;
from   ..events import BaseObject , EventHandler;


DEFAULT_PORT_ADDRESS  = 36061;
DEFAULT_MGS_LENGTH  = 1024;

class SignalHandler(object):
    def __init__(self):
        super().__init__();


class Client(object):
    def __init__(self, socket , address , status= True):
        if(isinstance(self.__Socket, socket.Socket) != True):
            raise TypeError("Expecting a python native socket.Socket object");
        self.__Socket   =  socket;
        self.__Address  =  address;
        self.__IsOpen   =  status;
        
    @property
    def Socket(self):
        return self.__Socket;
    
    def Close(self):
        if(self.Socket != None):
            self.Socket.close();
        self.__IsOpen = False;
            
    def Read(self):
        data  =  None;
        if(self.Socket != None):
            data = self.Socket.recv(DEFAULT_MGS_LENGTH, True);
            if(data == b''):
                self.Close();
                print("Closed");
        return data;

    def Write(self, buffer):
        if(self.Socket != None):
            self.Socket.send(buffer);
            
    @property
    def IsOpen(self):
        return self.__IsOpen;



class Handler(object):


    def __init__(self, client):
        self


class DaemonServer(object):

    __CLASS__     = None;
    __INSTANCE__  = None;

    #Implemeny single pattern in Python.
    def __new__(cls, *args, **kwargs):
        if(cls != None):
            # There is class for this Server
            # if this server have same address information
            cls.__CLASS__  =  cls;
            cls.__INSTANCE__  =  super().__new__(cls);
        return cls.__INSTANCE__;
        

    
    def __init__(self, **kwargs):
        self.__Port  = kwargs['port'] if(('port' in kwargs) and (type(kwargs['port']) == int)) else DEFAULT_PORT_ADDRESS;
        self.__StartLocker  =  Lock();
        self.__RunThread    = None;
        self.__IsRunning    = False;
        self.__CanStart     = False;
        self.__Socket       = None;
        self.__HostAddress  = None;
        self.__Clients      = list();
        self.ThreadPoles    = list();
        
    @property
    def Clients(self):
        return self.__Clients;
        
    @property
    def HostAddress(self):
        return self.__HostAddress;
    
    @HostAddress.setter
    def HostAddress(self, hostaddress):
        if(type(hostaddress) != str):
            raise ValueError("@Invalid hostaddress provided");
        if(self.IsRunning):
            print("Unable to set the host address while server is running");
            return ;
        else:
            self.__HostAddress = hostaddress;
    
    @property
    def Port(self):
        return self.__Port;

    @Port.setter
    def Port(self, value):
        if(self.IsRunning == True):
            print("Unable to change port when server is running");
            # Throw a message to the users;
            return ;
        if(type(value) != int):
            raise TypeError("@Port: expecting an integer value");
        self.__Port = value;

    def Start(self):
        self.__StartLocker.acquire();
        if(self.IsRunning == True):
            print("Unable to start server when server is already started");
            return ;
        if(self.__Socket == None):
            # Create TCP socket
            self.__Socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            if(self.HostAddress == None):
                self.HostAddress  = socket.gethostbyname(socket.gethostname());
            self.__Socket.bind((self.HostAddress, self.Port));
            self.__Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__RunThread = Thread(target  = self.__InBackground);
            self.__RunThread.daemon  = True;
            self.__RunThread.start();
        
    @property
    def IsRunning(self):
        return self.__IsRunning;

    @IsRunning.setter
    def IsRunning(self, value):
        if(type(value) == bool):
            if(value != self.__IsRunning):
                if( (value  == True) and (self.__CanStart == True)):
                    # I think user want to start the server by setting this property to true;
                    # The server is not running and this
                    self.Start();
                else:
                    if(self.__IsRunning):
                        # The server is running
                        if(value == True):
                            print("Unable to start server when server is already running");
                        else:
                            self.Stop(); # stop the server
                            
            self.__IsRunning  = value;
                    

    def __InBackground(self):

        self.__StartLocker.release();
        self.__IsRunning  = True;
        self.__CanStart   = False;
        print("Server started at : {0}:{1}".format(self.HostAddress, self.Port));
        while(self.IsRunning and (self.__Socket != None)):
            try:
                print("Waiting for connections: ");
                self.__Socket.listen(5);
                socket, address  = self.__Socket.accept(); 
                client  = Client(socket, address, True);
                self.Clients.append(client);
                print(client.Socket);
                newConnetionThread  =  Thread(target= self.OnNewConnection, args=(socket,));
                newConnetionThread.daemon  = False;
                newConnetionThread.start();
                self.ThreadPoles.append(newConnetionThread);
            except Exception as err:
                # Raise error events and terminate the server;
                if(self.IsRunning):
                    self.Stop();
                raise err;
            finally:
                #Remove all client and send and if possible send them
                # A server shutdow message
                self.__CleanUp();
                pass;

    def self.__CleanUp(self):
        for client in self.Clients:
            client.Close();
            print("Removing");
            print(client.Socket);

    def OnNewConnection(self,client):
        if(client != None):
            while(client.IsOpen):
                data  =   client.Read(DEFAULT_MGS_LENGTH, True);
                if(len(data) > 0):
                    print(data);
                    
                else:
                    client.Close();
            print("Closed");

    def Stop(self):
        self.__StartLocker.acquire();
        try:
            if(self.IsRunning):
                self.__IsRunning  = False;
                if(self.__RunThread.isAlive()):
                    self.__RunThread.join(1);
                if(self.__Socket != None):
                    # Close all client connections;
                    for client in self.Clients:
                        client.close();
                    self.__Socket.close();
               
        except Exception as err:
            print(err);
        finally:
            self.__RunThread  = None;
            self.__CanStart   = True;
        self.__StartLocker.release();

    




        

