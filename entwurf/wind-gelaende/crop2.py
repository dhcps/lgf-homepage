import numpy as np, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, LinearSegmentedColormap
M=np.load('mosaic.npy');z=14;mpp=6.434
def px(lat,lon):
  n=2**z;x=(lon+180)/360*n;r=math.radians(lat);y=(1-math.asinh(math.tan(r))/math.pi)/2*n
  return (y-5715)*256,(x-8712)*256
r0,c0=px(47.695,11.488);r1,c1=px(47.645,11.600)
r0,r1,c0,c1=map(int,(r0,r1,c0,c1));A=M[r0:r1,c0:c1];np.save('crop2.npy',A);print(A.shape)
import json;json.dump(dict(r0=r0,c0=c0),open('crop2.json','w'))
cm=LinearSegmentedColormap.from_list('t',['#C9D9C0','#9DBB8E','#6F9468','#8C8E78','#B9AFA0','#E9E6E0'])
rgb=LightSource(315,40).shade(A,cmap=cm,vert_exag=1.6,dx=mpp,dy=mpp,blend_mode='soft',vmin=650,vmax=1750)
W=A.shape[1]*mpp/1000;Hh=A.shape[0]*mpp/1000
fig,ax=plt.subplots(figsize=(12,8.4),dpi=160)
ax.imshow(rgb,extent=[0,W,Hh,0])
X=np.arange(A.shape[1])*mpp/1000;Y=np.arange(A.shape[0])*mpp/1000
cs=ax.contour(X,Y,A,levels=range(700,1800,50),colors='#2B3A33',linewidths=[.45 if l%100==0 else .2 for l in range(700,1800,50)],alpha=.55)
ax.clabel(cs,levels=range(800,1800,200),fmt='%d',fontsize=6.5,inline=True)
def lab(n,lat,lon,h=None,town=False,off=(6,6)):
  r,c=px(lat,lon);x=(c-c0)*mpp/1000;y=(r-r0)*mpp/1000
  ax.plot(x,y,'o' if town else '^',ms=5 if town else 6,color='#1D5E9E' if town else '#17212B')
  t=n+(f'\n{h} m' if h else '');ax.annotate(t,(x,y),xytext=off,textcoords='offset points',fontsize=8.5,color='#17212B',fontweight='normal' if town else 'bold',bbox=dict(boxstyle='round,pad=.25',fc='white',ec='none',alpha=.85))
lab('Brauneck',47.6638,11.524,1555)
lab('Latschenkopf',47.6571,11.4993,1712)
lab('Lenggries',47.6806,11.5736,town=True)
lab('Wegscheid',47.6620,11.5700,town=True)
lab('Draxlhang',47.66185,11.56482,town=True,off=(-58,-16))
r,c=px(47.6685,11.5587);x=(c-c0)*mpp/1000;y=(r-r0)*mpp/1000
ax.add_patch(plt.Circle((x,y),.45,fill=False,ec='#D9822B',lw=1.6,ls='--'));ax.annotate('die Nase?',(x+.45,y-.3),fontsize=9,color='#B5651D',fontweight='bold')
ax.annotate('N',(0.965,0.94),xycoords='axes fraction',ha='center',fontsize=12,fontweight='bold')
ax.annotate('',(0.965,0.93),(0.965,0.85),xycoords='axes fraction',arrowprops=dict(arrowstyle='-|>',color='#17212B'))
ax.set_xlabel('km');ax.set_ylabel('km')
ax.set_title('Latschenkopf bis Lenggries: Höhenmodell, Linien alle 50 m (ca. 30 m Auflösung)',loc='left',fontsize=11)
plt.tight_layout();plt.savefig('hoehenmodell-2.png')
