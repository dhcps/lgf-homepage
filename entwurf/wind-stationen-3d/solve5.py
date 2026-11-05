import numpy as np, math, json, base64, time
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import splu
from scipy import ndimage as nd
H5=np.load('H5.npy');W0,N0=686000,5286000
DE0,DE1,DN1,DN0=686500,695800,5285700,5279500
f=3;dx=15;H=nd.zoom(nd.uniform_filter(H5,f),1/f,order=1);ny,nx=H.shape
ci=lambda e,n,g:(int(round((N0-n)/g)),int(round((e-W0)/g)))
Ztop=2250.;T=Ztop-H;N=nx*ny;idx=np.arange(N).reshape(ny,nx)
Tx=(T[:,1:]+T[:,:-1])/2;Ty=(T[1:,:]+T[:-1,:])/2
I=idx[1:-1,1:-1].ravel();te=Tx[1:-1,1:];tw=Tx[1:-1,:-1];ts=Ty[1:,1:-1];tn=Ty[:-1,1:-1]
rows=np.concatenate([I]*5);cols=np.concatenate([idx[1:-1,2:].ravel(),idx[1:-1,:-2].ravel(),idx[2:,1:-1].ravel(),idx[:-2,1:-1].ravel(),I])
vals=np.concatenate([te.ravel(),tw.ravel(),ts.ravel(),tn.ravel(),-(te+tw+ts+tn).ravel()])
bd=np.ones((ny,nx),bool);bd[1:-1,1:-1]=False;B=idx[bd]
A=csr_matrix((np.concatenate([vals,np.ones(len(B))]),(np.concatenate([rows,B]),np.concatenate([cols,B]))),shape=(N,N)).tocsc()
t_=time.time();LU=splu(A);print('LU',time.time()-t_)
AGL=np.arange(0,425,50.);t0,t1=np.tan(np.radians(4)),np.tan(np.radians(14))
gl=60;Hl=nd.zoom(nd.uniform_filter(H5,12),1/12,order=1);YY,XX=np.mgrid[0:Hl.shape[0],0:Hl.shape[1]].astype(float)
lr0,lc0=ci(DE0,DN1,gl);lr1,lc1=ci(DE1,DN0,gl)
ug=45;r0,c0=ci(DE0,DN1,dx);r1,c1=ci(DE1,DN0,dx)
def enc(X,dt):return base64.b64encode(np.ascontiguousarray(X).astype(dt).tobytes()).decode()
fac0=np.clip(1+0.0012*(H-nd.uniform_filter(H,int(1200/dx))),0.6,1.6)
OUT=[]
for di in range(16):
  deg=di*22.5;th=math.radians(deg);wx,wy=-math.sin(th),math.cos(th);U,V=30*wx,30*wy
  b=np.zeros(N);b[I]=-(V*(ts-tn)*dx+U*(te-tw)*dx).ravel()
  phi=LU.solve(b).reshape(ny,nx);gy,gx=np.gradient(phi,dx);u=U+gx;v=V+gy
  L=np.zeros((len(AGL),)+Hl.shape)
  for k in range(1,int(1300/gl)+1):
    dd=k*gl;up=np.full(Hl.shape,-1e9)
    for lat in np.linspace(-1,1,5):
      off=lat*dd*math.tan(math.radians(14))
      up=np.maximum(up,nd.map_coordinates(Hl,[YY-k*wy+off*wx/gl,XX-k*wx-off*wy/gl],order=1,mode='nearest'))
    for ai,agl in enumerate(AGL):
      s=(up-(Hl+agl))/dd;L[ai]=np.maximum(L[ai],np.clip((s-t0)/(t1-t0),0,1)*np.clip(1.3-dd/1300,0,1))
  L0=nd.zoom(L[0],gl/dx,order=1);L0=np.pad(L0,((0,max(0,ny-L0.shape[0])),(0,max(0,nx-L0.shape[1]))),mode='edge')[:ny,:nx]
  fac=fac0*(1-0.5*L0);u*=fac;v*=fac
  OUT.append(dict(deg=deg,u=enc(np.round(u[r0:r1:3,c0:c1:3]*100),np.int16),v=enc(np.round(v[r0:r1:3,c0:c1:3]*100),np.int16),l3=enc(L[:,lr0:lr1,lc0:lc1]*250,np.uint8)))
  print(di,round(time.time()-t_,1))
mg=20;Hm=nd.zoom(nd.uniform_filter(H5,4),1/4,order=1);mr0,mc0=ci(DE0,DN1,mg);mr1,mc1=ci(DE1,DN0,mg);Hm=Hm[mr0:mr1+1,mc0:mc1+1]
D=dict(ny=len(range(r0,r1,3)),nx=len(range(c0,c1,3)),dx=ug,lny=lr1-lr0,lnx=lc1-lc0,lnz=len(AGL),ldz=50,ldx=gl,mny=Hm.shape[0],mnx=Hm.shape[1],mdx=mg,h=enc(np.round(Hm*10),np.uint16),dirs=OUT)
json.dump(D,open('field5.json','w'));print(len(json.dumps(D))//1024,'KB')
