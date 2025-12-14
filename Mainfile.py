import logelement

elNot = logelement.TNot()
elAnd = logelement.TAnd()
elAnd.link(elNot, 1)
print(" A | B | not(A&B) ")
print("------------------")
for A in range(2):
    elAnd.In1 = bool(A)
    for B in range(2):
        elAnd.In2 = bool(B)
        elNot.In1 = elAnd.Res
        print(" ", A, "|", B, "|", int(elNot.Res))


elNot1 = logelement.TNot()
elNot2 = logelement.TNot()
elAnd1 = logelement.TAnd()
elAnd2 = logelement.TAnd()
elOr = logelement.TOr()

elNot1.link(elAnd1, 2)
elNot2.link(elAnd2, 1) 

elAnd1.link(elOr, 1) # a и -b
elAnd2.link(elOr, 2) # -a и b

# (а и -b) или (-а и b)
print("XOR XOR XOR XOR")
print(" A | B | XOR ")
print("-------------")
for A in range(2):
    for B in range(2):
        elNot2.In1 = bool(A) # -a
        elAnd1.In1 = bool(A) # a и -b
        elNot1.In1 = bool(B) # -b
        elAnd2.In2 = bool(B) # -a и b
        print(" ", A, "|", B, "|   ", int(elOr.Res))
