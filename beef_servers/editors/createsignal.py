import wx;


class CreateSignalPanel(wx.Panel):
    UPDATE_BUTTON     =  0x1001;
    SIGNAL_NAME_ID    =  0x1002;
    SIGNAL_COMBOX_ID  = 0x1003;
    def __init__(self, parent, ):
        super().__init__(parent, id= wx.ID_ANY, style=wx.SIMPLE_BORDER);
        sizer =  wx.BoxSizer(wx.VERTICAL);
        # Create a title panel that will take the first row.
        self.UIDefaultFont    = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL, False);
        self.SetFont(self.UIDefaultFont);
        sizer.AddSpacer(10);
        #Create the component module name;
        pnlComboxModule =  wx.Panel(self, wx.ID_ANY);
        # Add Signal Text for the signal Name
        pnlSignalPanel  =  wx.Panel(self, wx.ID_ANY);
        pnlSignalPanelSizer =  wx.BoxSizer(wx.HORIZONTAL);
        pnlSignalPanelSizer.AddSpacer(40);
        lblSignals    =  wx.StaticText(pnlSignalPanel, label  = "Signal Name" , size = wx.Size(100,28));
        pnlSignalPanelSizer.Add(lblSignals);
        self.__txtSignals    =  wx.TextCtrl( pnlSignalPanel, id =self.SIGNAL_COMBOX_ID, size =  wx.Size(330,28));
        pnlSignalPanelSizer.Add(self.__txtSignals);
        pnlSignalPanel.SetSizer(pnlSignalPanelSizer);
        sizer.Add(pnlSignalPanel);
        sizer.AddSpacer(2);
        # Create text for the signal pin
        pnlSignalTextEditor       = wx.Panel(self, wx.ID_ANY);
        pnlSignaltextEditorSizer  = wx.BoxSizer(wx.HORIZONTAL);
        pnlSignaltextEditorSizer.AddSpacer(40);
        lblSignalPin  =  wx.StaticText(pnlSignalTextEditor, id  = wx.ID_ANY, label = "Pin Number" , size = wx.Size(100,28));
        pnlSignaltextEditorSizer.Add(lblSignalPin);
        self.__txtSignalPin  =  wx.TextCtrl(pnlSignalTextEditor,  id = self.SIGNAL_NAME_ID, size = wx.Size(100,28));
        pnlSignaltextEditorSizer.Add(self.__txtSignalPin);
        pnlSignalTextEditor.SetSizer(pnlSignaltextEditorSizer);
        sizer.Add(pnlSignalTextEditor);

        sizer.AddSpacer(2);
        # Add update buttons and delete signal buttons. 
        self.__panelOperations =  wx.Panel(self, wx.ID_ANY);
        contentSizer =  wx.BoxSizer(wx.HORIZONTAL);
        self.__panelOperations.SetSizer(contentSizer);
        self.__createSignalButton =  wx.Button(self.__panelOperations, id =  self.UPDATE_BUTTON , label = "Create",size= wx.Size(100 , 30));
        
        contentSizer.AddSpacer(139);
        contentSizer.Add(self.__createSignalButton, flag = wx.RIGHT| wx.TOP);
        sizer.Add(self.__panelOperations);
        self.SetSizer(sizer);
      
        #Handle Events
        self.HandleEvents();
    def HandleEvents(self):    
        self.__createSignalButton.Bind(wx.EVT_BUTTON, self.OnSignalCreateRequest);
       

    def OnSignalCreateRequest(self, event):
        name =  self.__txtSignals.GetValue();
        pin  =  self.__txtSignalPin.GetValue();
        print(name, pin);
