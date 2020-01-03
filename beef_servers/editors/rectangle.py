import wx;

class Rectangle(wx.Rect):
    
    def __init__(self, pos, size):
        super().__init__(pos, size);

    @property
    def Area(self):
        return self.Width * self.Height;

    @property
    def Location(self):
        return self.Position;
        
    def __str__(self):
        return "(pos{0}, size{1})".format(self.Location , self.Size);


    def Create(x,  y, width , height):
        return Rectangle(wx.Point(x, y), wx.Size(width, height));


    def IntersectWith(self, point):
       xContains =   (point.x >= self.X) and (point.x <= (self.X + self.Width));
       yContains  =  (point.y >= self.Y) and (point.y <= (self.Y + self.Height));

       return ((xContains ==  True) and (yContains  == True))
       


    def Intersect(self, rect):
        status = False;

        if(isinstance(rect, Rectangle)):
           #find if rect.position is within
            status  =  self.IntersectWith(rect.Location) or self.IntersectWith(wx.Point(rect.Right, rect.Bottom));
            if(status != True):
                status  = rect.IntersectWith(self.Location) or rect.IntersectWith(wx.Point(self.Right, self.Bottom));

        return status;
    

  
    


if(__name__ =='__main__'):
    #Intersect (166, 145) in (pos(137, 63), size(40, 10))

    #Testing for rectangle intersection
    rect = Rectangle.Create(20, 10, 600,800);
    print(rect);
    r1  = Rectangle.Create(137, 63, 40, 10);
    r2  = Rectangle.Create(710,10,0,0);
    print(r1.Intersect(r2));


    #test for point

    if(r1.IntersectWith(wx.Point(166, 145))):
       print("Point found");



    #Find Area

    print("{0} area".format(r1.Area));
















    
