class point():
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y and self.z==other.z:
            return True
        else: return False


class ploygon():

    def __init__(self,points):
        self.p=[]
        for point in points:
            self.p.append(point)

    def neighbour(self,ploygon2):
        flag=False
        for p1 in self.p:
            for p2 in ploygon2.p:
                if p1==p2:
                    flag=True
                    break
        return flag

    def __str__(self):
        print('(   ')
        for point in self.p:

            print('(%f,%f,%f)'%(point.x,point.y,point.z))
        print('   )')

    def __repr__(self):
        print('(   ')
        for point in self.p:
            print('(%f,%f,%f)' % (point.x, point.y, point.z))
        print('   )')




U=set()
already_in=list()


def FindWalls():
    global first_wall
    global U
    found_wall=first_wall

    newed=True

    while(newed==True):
        newed=False
        already_in.append(found_wall)
        U.remove(found_wall)
        for wall in U:
            if found_wall.neighbour(wall):
                found_wall=wall
                newed=True
                break



x1=point(0,0,0)
x2=point(0,0,1)
x3=point(0,1,0)
x4=point(0,1,1)
x5=point(1,0,0)
x6=point(1,0,1)
x7=point(1,1,0)
x8=point(1,1,1)

s1=ploygon([x1,x2,x3,x4])
s2=ploygon([x5,x6,x7,x8])
s3=ploygon([x1,x3,x5,x7])
s4=ploygon([x2,x4,x6,x8])

U=set([s1,s2,s3,s4])
first_wall=s1
FindWalls()
print(already_in)