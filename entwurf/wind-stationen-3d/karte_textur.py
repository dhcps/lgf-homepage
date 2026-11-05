import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, LinearSegmentedColormap
from scipy import ndimage as nd
H=np.load('H5.npy');W0,N0=686000,5286000
DE0,DN1=686500,5285700;mny,mnx=311,466
A=H[(N0-DN1)//5:(N0-DN1)//5+(mny-1)*4+1,(DE0-W0)//5:(DE0-W0)//5+(mnx-1)*4+1]
As=nd.gaussian_filter(A,5.0)  # leichte Glättung für die Schummerung
A2=nd.zoom(As,2,order=1)
cm=LinearSegmentedColormap.from_list('t',['#C9D9C0','#9DBB8E','#6F9468','#8C8E78','#B9AFA0','#E9E6E0'])
rgb=LightSource(315,40).shade(A2,cmap=cm,vert_exag=1.4,dx=2.5,dy=2.5,blend_mode='soft',vmin=650,vmax=1750)
h,w=A2.shape;dpi=100
fig=plt.figure();fig.set_size_inches(4096/dpi,4096*h/w/dpi)
ax=fig.add_axes([0,0,1,1]);ax.imshow(rgb,extent=[0,w,h,0],interpolation='bilinear');ax.set_axis_off()
Ac=nd.gaussian_filter(A,7.0)  # ~35 m: sanfte Höhenlinien
lv=list(range(700,1800,50));X=np.arange(A.shape[1])*2;Y=np.arange(A.shape[0])*2
ax.contour(X,Y,Ac,levels=lv,colors='#2B3A33',linewidths=[.8 if l%100==0 else .35 for l in lv],alpha=.45,antialiased=True)
ax.set_xlim(0,w);ax.set_ylim(h,0)
fig.savefig('../karte_tex.jpg',dpi=dpi,pil_kwargs={'quality':88});print('ok')
