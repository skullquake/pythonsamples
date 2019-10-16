class Person:
    """
    An example 'plain' (class) to create 'Person' objects
    """
    def __init__(self,name="<unknown>"):
        """
        Person 'constructor'/'initializer'
        :param str name: Name of new 'Person'. Default '<unknown>'
        """
        self.__name=name
    def __str(self):
        """
        Override convertion to string ('str')
        """
        return "Name: {}".format(self.__name)
    def __repr__(self):
        """
        Accessor ('mutator') for the name of the 'Person'.
        :param str name: New value for the '__name__' data member.
        """
        self.__name=name
    def get_name(self):
        """
        Accessor ('getter') for the name of 'Person'.
        """
        return self.__name
    def greet(self,greeting="Hello, World"):
        """
        'Custom' method, specific to 'Person' objects.
        :param str greeting: Optional greeting as part of message.
        """
        print("{}! I'm {}.".format(greeting,self.__name))
