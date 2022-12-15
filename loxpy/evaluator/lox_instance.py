'''
Runtime representation of an instance
'''

class LoxInstance:
    
    def __init__(self, klass):
        self.kclass = klass

    def __str__(self):
        return self.kclass.name + " instance"
