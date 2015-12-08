__author__ = 'Nikel'

class B: pass

class A(B): pass

# A.mro()
# Error will be raised
# there is no diamond structure problem

class A1(object): pass

for cls in A1.mro():
    print cls.__name__, ' ',

# >>> A1 object

print '\n'

class C2(object): pass

class B2(C2): pass

class E2(object): pass

class D2(E2): pass

class A2(B2, D2): pass

for cls in A2.mro():
    print cls.__name__, ' ',

# >>> A2 B2 C2 D2 E2 object

print '\n'

class E3(object): pass

class D3(object): pass

class F3(object): pass

class B3(E3, D3): pass

class C3(D3, F3): pass

class A3(B3, C3): pass

for cls in A3.mro():
    print cls.__name__, ' ',

# >>> A3 B3 E3 C3 D3 F3 object