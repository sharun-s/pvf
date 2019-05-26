# from https://stackoverflow.com/questions/19329039/plotting-animated-quivers-in-python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import pandas as p
from pvfdefaults import partyangle, partycolor
import sys
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from math import radians, cos, sin

maketrail = False
#partyangle['INC']=180
norm = Normalize(vmin=0.0, vmax=11.0)

#m = p.read_csv("apur.tsv", delimiter='\t')
m = p.read_csv("apur.csv")
district = sys.argv[1] # district name eg Tadipatri
d = m[m.name == district]
# get the 3 largest votes polled per year
dgindex = d.groupby('year').votes.nlargest(3).index
vectors = m.iloc[dgindex.levels[1]][['year','abr','votes']]
years = dgindex.levels[0]


#X, Y = np.mgrid[:2*np.pi:1j,:2*np.pi:1j]
X,Y= [0,0,0,0], [0,0,0,0]
#U = np.cos(X)
#V = np.sin(Y)
tmp = vectors[vectors.year == years[0]]
A = [ (cos(radians(partyangle[i])), sin(radians(partyangle[i]))) for i in tmp.abr ]
#A.insert(0,(1.0, 0.))

U,V=[],[]
for i, cnt in enumerate(tmp.votes):
    U.append( cnt*A[i][0] )
    V.append( cnt*A[i][1] )

U.insert(0, 0)
U.insert(0, 0)

V.insert(0, 0)
V.insert(0, 0)

C = [partycolor[i] for i in tmp.abr]
C.insert(0, 0.)
C.insert(0, 11.)
uall = [0]
vall = [0]

fig, (ax, line) = plt.subplots(1,2)
plt.set_cmap(cm.Paired)

#fig = plt.figure(figsize=(6, 6))
#ax = fig.add_axes([0, 0, 1, 1])

#units - arrow dimensions
#print(U)
#print(V)
Q = ax.quiver(X, Y, U, V,C, scale=200000)
K, =line.plot(uall, vall, 'r')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
line.grid()


def update_quiver(num, Q, X, Y):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    idx = num % len(years) #cause the first plot has already be drawn
    #print(idx)

    tmp = vectors[vectors.year == years[idx]]
    A = [ (cos(radians(partyangle[i])), sin(radians(partyangle[i])), partycolor[i]) for i in tmp.abr ]
    #A.insert(0,(1.0, 0.))

    U, V, C =[], [], []
    for i, cnt in enumerate(tmp.votes):
        U.append( cnt*A[i][0] )
        V.append( cnt*A[i][1] )
        C.append( A[i][2] ) 
    C.insert(0, 11.)
    V.insert(0, 0)
    U.insert(0, 0)
    #uall.append(0)
    #vall.append(0)
    if not maketrail:
        uall = [0]
        vall = [0]
    allv = list(zip(U,V))
    sumx = allv[0][0]
    sumy = allv[0][1]
    #uall.append(sumx)
    #vall.append(sumy)
    for i in range(1,len(allv)):
       sumx = sumx + allv[i][0]
       sumy = sumy + allv[i][1]
    Q.set_UVC(U,V, C)
    uall.append(sumx)
    vall.append(sumy)
    
    line.plot(uall, vall, 'r')
    xmin, xmax = line.get_xlim()
    ymin, ymax = line.get_ylim()
    limitchanged=False
    if sumx >= xmax:
        line.set_xlim(xmin, 2*xmax)
        limitchanged = True
    if sumy >= ymax:
        line.set_ylim(ymin, 2*ymax)
        limitchanged = True
    if limitchanged:
        line.figure.canvas.draw()
    #K.set_xdata(uall)
    #K.set_ydata(vall)
    #ltxt = str(years[idx])+' '+'{:.2f}'.format(sumx)+' '+ '{:.2f}'.format(sumy)
    ltxt = str(years[idx])
    flip = 1 if (num % 2) == 1 else -1
    line.annotate(ltxt, xy=(sumx, sumy), xytext=(sumx+flip*5000*2, sumy+flip*5000*2), 
                bbox=dict(boxstyle="round", fc='blue', alpha=0.4))
    line.figure.canvas.draw()

    return Q,

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver, len(years), repeat=False,
    fargs=(Q, X, Y),
    interval=550, blit=False)
#fig.tight_layout()
plt.show()


#https://stackoverflow.com/questions/27820447/how-should-i-go-about-animating-particles-in-python-matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# fig, ax = plt.subplots()
# points, = ax.plot(np.random.rand(10), 'o')
# ax.set_ylim(0, 1)

# def update(data):
#     points.set_ydata(data)
#     return points,

# def generate_points():
#     while True:
#         yield np.random.rand(10)  # change this

# ani = animation.FuncAnimation(fig, update, generate_points, interval=300)
# ani.save('animation.gif', writer='imagemagick', fps=4);
# plt.show()
