class print_debug:
    
    def __init__(self,name,color=97):

        self.name="["+name+"]"
        self.color_name = "\x1b["+str(color)+"m"

        self.GREY = "\x1b[97m"
        self.GREEN = "\x1b[92m"
        self.ORANGE = "\x1b[33m"
        self.BLUE = "\x1b[34m"
        self.YELLOW = "\x1b[33m"
        self.RED = "\x1b[91m"
        self.BOLD_RED = "\x1b[31;1m"
        self.REVERSE = "\x1b[07m"
        self.RESET = "\x1b[0m"

    def debug(self,text):
        print(self.color_name + self.name +"[DEBUG]" + text + self.RESET)

    def info(self,text):
        print(self.color_name + self.name + self.GREEN +"[INFO]" + text + self.RESET)

    def warning(self,text):
        print(self.color_name + self.name + self.YELLOW +"[WARNING]" + text + self.RESET)

    def error(self,text):
        print(self.color_name + self.name + self.RED +"[ERROR]" + text + self.RESET)

    def critical(self,text):
        print(self.color_name + self.name + self.BOLD_RED +"[CRITICAL]" + text + self.RESET)

