class A:
    
    def __repr__(self):
        print(1)
        return('repr')
    
    def __str__(self):
        print(2)
        return 'str'

class B:
    
    def __repr__(self):
        print(1)
        return('repr')

class C:
    
    def __str__(self):
        print(2)
        return 'str'

a, b, c = A(), B(), C()

print(a)