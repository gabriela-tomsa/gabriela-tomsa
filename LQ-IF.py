def isoscel(a,b,c):
    if a<=0 or b<=0 or c<=0: print("Nu formeaza triunghi")
    elif a==b or a==c or b==c:
        if a==b and a+b<c: print("Nu formeaza triunghi")
        elif a==c and a+c<b: print("Nu formeaza triunghi")
        elif b==c and b+c<a: print("Nu formeaza triunghi")
        elif a==b and b==c: print("Nu formeaza triunghi isoscel")
        else: print("Formeaza triunghi isoscel")
    else: print("Nu formeaza triunghi isoscel")


isoscel(5,15,5)
