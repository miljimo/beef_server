from beef_servers.servers import DaemonServer;


if(__name__ =="__main__"):
    server = DaemonServer();
    server.Start();
    try:
        while(server.IsRunning):
            pass;
        server.Stop();
    except Exception as err:
        print("Stop unexceptedly - {0}".format(err));
    finally:
        server.Stop();
