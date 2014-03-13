#########################################################################
# graphics.py
# Lisa Torrey
# An interface for Python graphics (a simple wrapper for Tkinter).
#
# To create and use a display window:
#
#   Display(color, width, height)
#
#   add(item): add an item to the display
#   remove(item): remove an item from the display
#   contains(item): check if an item is displayed
#
#   draw(): draw everything for the first time
#   is_open(): check if the display is still open
#   update(time): wait this many milliseconds, then update the display
#   close(): close the display
#
#   set_left_click_handler(function): make this function handle left clicks
#   set_right_click_handler(function): make this function handle right clicks
#   set_drag_handler(function): make this function handle left-mouse drags
#   set_key_handler(function): make this function handle key presses
#
# To create items that can be added to the display:
#
#   Oval(color, left_x, top_y, right_x, bottom_y)
#   Rectangle(color, left_x, top_y, right_x, bottom_y)
#   Line(color, x1, y1, x2, y2, ...)
#   Polygon(color, x1, y1, x2, y2, ...)
#   Image(filename, center_x, center_y)
#   Text(string, center_x, center_y, [color, size])
#   InputBox(width_in_characters, initial_string, center_x, center_y)
#   Button(string, color, left_x, top_y, right_x, bottom_y, [textcolor, textsize])
#
# Things you can do with any of these items:
#
#   get_coords()                Get/set an item's coordinates.
#   set_coords(x, y, ...)
#
#   get_speed()                 Get/set an item's speed.
#   set_speed(vx, vy)
#
#   get_color()                 Get/set an item's color.
#   set_color(color)
#
#   move()                      Move this item according to its speed
#   contains(x,y)               Check if a point falls inside this item.
#   overlaps(other_item)        Check if another item overlaps with this item.
#
# Things you can do only with certain types of items:
#
#   get_text()                  Get/set the text of a Text, InputBox, or Button.
#   set_text(string)
#
#   get_filename()              Get/set the GIF filename of an Image.
#   set_filename(filename)
#
#   get_pixel(x, y)             Get/set the RGB color at pixel x,y of an Image.
#   set_pixel(x, y, r, g, b)
#
#   get_width()                 Get/set the width or height of an Image.
#   get_height()   
#   set_width(w)
#   set_height(h)
#
#########################################################################

from Tkinter import *

# An object that displays a graphical window
class Display:

    # Create a Display object with this background color, width, and height
    def __init__(self, color, width, height):
        self.width = width
        self.height = height

        # Set up a Tk window
        self.window = Tk()
        self.window.wm_geometry(str(width)+"x"+str(height)+"+100+100")
        self.window.wm_title("Sudoku Solver")
        self.canvas = Canvas(self.window, background=color, width=width, height=height)

        # Bind event for window closing
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # Keep track of items and whether canvas is open
        self.items = []
        self.open = True

    # Add an item to the display
    def add(self, item):
        if isinstance(item, Oval):
            item.handle = self.canvas.create_oval(item.coords, fill=item.color)
        elif isinstance(item, Line):
            item.handle = self.canvas.create_line(item.coords, fill=item.color)
        elif isinstance(item, Rectangle):
            item.handle = self.canvas.create_rectangle(item.coords, fill=item.color)
        elif isinstance(item, Polygon):
            item.handle = self.canvas.create_polygon(item.coords, fill=item.color)
        elif isinstance(item, Image):
            item.handle = self.canvas.create_image(item.coords, image=item.image)
        elif isinstance(item, Text):
            item.handle = self.canvas.create_text(item.coords, text=item.text, fill=item.color, font=("Times", item.size))
        elif isinstance(item, InputBox):
            item.box = Entry(self.window, width=item.width)
            item.set_text(item.text)
            item.handle = self.canvas.create_window(item.coords, window=item.box)
        elif isinstance(item, Button):
            item.handle = self.canvas.create_rectangle(item.coords, fill=item.color)
            item.text_handle = self.canvas.create_text(item.text_coords, text=item.text, fill=item.textcolor, font=("Times", item.textsize))
        else:
            print "Error! Not an object you can add to the display:", item
            return
        self.items.append(item)
        item.display = self

    # Remove an item from the display
    def remove(self, item):
        if self.open and item in self.items:
            self.items.remove(item)
            self.canvas.delete(item.handle)
            if isinstance(item, Button):
                self.canvas.delete(item.text_handle)

    # Check if an item is displayed
    def contains(self, item):
        if self.open and item in self.items:
            return True
        else:
            return False
    
    # Draw everything
    def draw(self):
        if self.open:
            self.canvas.pack()
            self.canvas.update()

    # Check if the display is still open
    def is_open(self):
        return self.open

    # Wait this many milliseconds, then update the display
    def update(self, time):
        if self.open:
            self.canvas.after(time)
            self.canvas.update()
    
    # Close the display
    def close(self):
        self.window.destroy()
        self.open = False

    # Make this function handle left clicks
    def set_left_click_handler(self, function):
        self.window.bind("<Button-1>", function)

    # Make this function handle right clicks
    def set_right_click_handler(self, function):
        self.window.bind("<Button-3>", function)

    # Make this function handle left-mouse drags
    def set_drag_handler(self, function):
        self.window.bind("<B1-Motion>", function)

    # Make this function handle key presses
    def set_key_handler(self, function):
        self.window.bind("<Key>", function)

# An object that represents any display item
class Item():
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.vx, self.vy = 0, 0
        self.handle = None
        self.display = None

    # Access the coordinates of this item
    def get_coords(self):
        coordlist = list(self.coords)
        for i in range(len(coordlist)):
            coordlist[i] = int(round(coordlist[i]))
        coordtuple = tuple(coordlist)
        return coordtuple

    # Change the coordinates of this item
    def set_coords(self, *coords):
        self.coords = coords
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.coords(self.handle, *coords)

    # Access the vx,vy speed of this item
    def get_speed(self):
        return self.vx, self.vy

    # Change the speed of this item
    def set_speed(self, vx, vy):
        self.vx = vx
        self.vy = vy

    # Move this item according to its speed
    def move(self):
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.move(self.handle, self.vx, self.vy)
            self.coords = self.display.canvas.coords(self.handle)       

    # Access the color of this item
    def get_color(self):
        return self.color

    # Change the color of this item
    def set_color(self, color):
        self.color = color
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.itemconfig(self.handle, fill=color)
    
    # Check if a point falls approximately inside this item.
    def contains(self, x, y):
        if self.display != None and self.display.open and self in self.display.items:
            left, top, right, bottom = self.display.canvas.bbox(self.handle)
            return x > left and x < right and y > top and y < bottom
        return False

    # Check if another item overlaps approximately with this item
    def overlaps(self, other_item):
        if self.display != None and self.display.open and self in self.display.items and other_item in self.display.items:
            left, top, right, bottom = self.display.canvas.bbox(self.handle)
            return other_item.handle in self.display.canvas.find_overlapping(left+2, top+2, right-2, bottom-2)
        return False

# An object that represents an oval shape
class Oval(Item):

    # Create an Oval with this color and these coordinates
    def __init__(self, color, left_x, top_y, right_x, bottom_y):
        coords = left_x, top_y, right_x, bottom_y
        Item.__init__(self, color, coords)

# An object that represents a rectangle shape
class Rectangle(Item):

    # Create a Rectangle with this color and these coordinates
    def __init__(self, color, left_x, top_y, right_x, bottom_y):
        coords = left_x, top_y, right_x, bottom_y
        Item.__init__(self, color, coords)

# An object that represents a line shape
class Line(Item):

    # Create a Line with this color and these coordinates (x1,y1,x2,y2,...)
    def __init__(self, color, *coords):
        Item.__init__(self, color, coords)

# An object that represents a polygon shape
class Polygon(Item):

    # Create a Polygon with this color and these coordinates (x1,y1,x2,y2,...)
    def __init__(self, color, *coords):
        Item.__init__(self, color, coords)

# An object that represents a GIF image
class Image(Item):

    # Create an Image with this GIF file and center coordinates
    # Use a filename of None to get an empty 1-pixel image 
    def __init__(self, filename, center_x, center_y):
        coords = center_x, center_y
        Item.__init__(self, None, coords)
        self.source = filename
        if filename != None:
            self.image = PhotoImage(file=filename)
        else:
            self.image = PhotoImage(width=1, height=1)

    # Access the pixel width of this Image
    def get_width(self):
        return self.image.width()

    # Change the pixel width of this Image
    def set_width(self, w):
        self.image.configure(width=w)

    # Access the pixel height of this Image
    def get_height(self):
        return self.image.height()

    # Change the pixel height of this Image
    def set_height(self, h):
        self.image.configure(height=h)

    # Access the GIF file of this Image
    def get_filename(self):
        return self.source

    # Change the GIF file of this Image
    def set_filename(self, filename):
        self.source = filename
        self.image = PhotoImage(file=filename)
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.itemconfig(self.handle, image=self.image)

    # Access the RGB color at pixel x,y of this Image
    def get_pixel(self, x, y):
        pixel = self.image.get(x, y)
        return tuple(map(int, pixel.split()))

    # Change the RGB color at pixel x,y of this Image
    def set_pixel(self, x, y, r, g, b):
        self.image.put("#%02x%02x%02x" % (r, g, b), (x, y))

    # Do nothing since an Image doesn't have a single color
    def get_color(self):
        return None
    def set_color(self, color):
        pass
    
# An object that represents a text string
class Text(Item):

    # Create a Text of this string and center coordinates
    # Optional arguments for text color and size
    def __init__(self, string, center_x, center_y, color="black", size=12):
        coords = center_x, center_y
        Item.__init__(self, color, coords)
        self.text = string
        self.color = color
        self.size = size
    
    # Access the text string of this Text
    def get_text(self):
        return self.text

    # Change the text string of this Text
    def set_text(self, string):
        self.text = string
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.itemconfig(self.handle, text=string)

# An object that represents a box to type in
class InputBox(Item):

    # Create an InputBox with this character width, initial text, and center coordinates
    def __init__(self, width_in_characters, initial_string, center_x, center_y):
        coords = center_x, center_y
        Item.__init__(self, None, coords)
        self.width = width_in_characters
        self.text = initial_string
        self.box = None

    # Access the text string of this InputBox
    def get_text(self):
        return self.box.get()

    # Change the text string of this InputBox
    def set_text(self, string):
        self.box.delete(0, END)
        self.box.insert(0, string)

# An object that represents a button to click on
class Button(Item):

    # Create a Button with this text label, background color, and coordinates
    # Optional arguments for text color and size
    def __init__(self, string, color, left_x, top_y, right_x, bottom_y, textcolor="black", textsize=12):
        coords = left_x, top_y, right_x, bottom_y
        Item.__init__(self, color, coords)
        self.text = string
        self.textcolor = textcolor
        self.textsize = textsize
        self.text_coords = (self.coords[0] + self.coords[2]) / 2, (self.coords[1] + self.coords[3]) / 2
        self.text_handle = None

    # Access the text string of this Button
    def get_text(self):
        return self.text

    # Change the text string of this Button
    def set_text(self, string):
        self.text = string
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.itemconfig(self.text_handle, text=string)

    # Change the coordinates of this Button
    def set_location(self, *coords):
        self.coords = coords
        self.text_coords = (self.coords[0] + self.coords[2]) / 2, (self.coords[1] + self.coords[3]) / 2
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.coords(self.handle, *coords)
            self.display.canvas.coords(self.text_handle, self.text_coords)

    # Move this Button according to its speed
    def move(self):
        Item.move(self)
        if self.display != None and self.display.open and self in self.display.items:
            self.display.canvas.move(self.text_handle, self.vx, self.vy)
            self.text_coords = self.display.canvas.coords(self.text_handle)
