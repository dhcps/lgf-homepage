import numpy as np, math, json, base64
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy import ndimage as nd
M=np.load('mosaic.npy');z=14
def px(lat,lon):
  n=2**z;x=(lon+180)/360*n;r=math.radians(lat);y=(1-math.asinh(math.tan(r))/math.pi)/2*n
  return (y-5715)*256,(x-8712)*256
R0,C0=map(int,px(47.7085,11.465));R1,C1=map(int,px(47.640,11.612))
f=4;S=M[R0:R1,C0:C1];H=nd.zoom(nd.uniform_filter(S,f),1/f,order=1);ny,nx=H.shape;dx=6.434*f
r0,c0=px(47.695,11.488);r1,c1=px(47.645,11.600)
a=int((r0-R0)/f);b_=int((r1-R0)/f);c=int((c0-C0)/f);d_=int((c1-C0)/f)
crop=lambda X:X[...,a:b_,c:d_]
Ztop=2150.;T=Ztop-H;N=nx*ny;idx=np.arange(N).reshape(ny,nx)
Tx=(T[:,1:]+T[:,:-1])/2;Ty=(T[1:,:]+T[:-1,:])/2
I=idx[1:-1,1:-1].ravel();te=Tx[1:-1,1:];tw=Tx[1:-1,:-1];ts=Ty[1:,1:-1];tn=Ty[:-1,1:-1]
rows=np.concatenate([I]*5);cols=np.concatenate([idx[1:-1,2:].ravel(),idx[1:-1,:-2].ravel(),idx[2:,1:-1].ravel(),idx[:-2,1:-1].ravel(),I])
vals=np.concatenate([te.ravel(),tw.ravel(),ts.ravel(),tn.ravel(),-(te+tw+ts+tn).ravel()])
bd=np.ones((ny,nx),bool);bd[1:-1,1:-1]=False;B=idx[bd]
A=csr_matrix((np.concatenate([vals,np.ones(len(B))]),(np.concatenate([rows,B]),np.concatenate([cols,B]))),shape=(N,N))
AGL=np.arange(0,425,25.);t0,t1=np.tan(np.radians(4)),np.tan(np.radians(14))
Hl=H[::2,::2];gl=dx*2;YY,XX=np.mgrid[0:Hl.shape[0],0:Hl.shape[1]].astype(float)
def enc(X,dt):return base64.b64encode(X.astype(dt).tobytes()).decode()
OUT={}
for name,deg in (('NNW',340),('N',0),('NNO',20)):
  th=math.radians(deg);wx,wy=-math.sin(th),math.cos(th)  # Wind weht nach (x Ost, y Süd)
  U,V=30*wx,30*wy
  b=np.zeros(N);b[I]=-(V*(ts-tn)*dx+U*(te-tw)*dx).ravel()
  phi=spsolve(A,b).reshape(ny,nx);gy,gx=np.gradient(phi,dx);u=U+gx;v=V+gy
  # 3D lee
  L=np.zeros((len(AGL),)+Hl.shape)
  for k in range(1,int(1300/gl)+1):
    dd=k*gl;up=np.full(Hl.shape,-1e9)
    for lat in np.linspace(-1,1,5):
      off=lat*dd*math.tan(math.radians(14))
      sy=YY-k*wy+off*wx/gl;sx=XX-k*wx-off*wy/gl
      up=np.maximum(up,nd.map_coordinates(Hl,[sy,sx],order=1,mode='nearest'))
    for ai,agl in enumerate(AGL):
      s=(up-(Hl+agl))/dd
      L[ai]=np.maximum(L[ai],np.clip((s-t0)/(t1-t0),0,1)*np.clip(1.3-dd/1300,0,1))
  L0=nd.zoom(L[0],2,order=1)[:H.shape[0],:H.shape[1]]
  fac=np.clip(1+0.0012*(H-nd.uniform_filter(H,int(1200/dx))),0.6,1.6)*(1-0.5*L0)
  u*=fac;v*=fac
  la,lb,lc,ld=a//2,b_//2,c//2,d_//2
  Lc=L[:,la:lb,lc:ld]
  OUT[name]=dict(deg=deg,u=enc(np.round(crop(u)*100),np.int16),v=enc(np.round(crop(v)*100),np.int16),l3=enc(Lc*250,np.uint8))
  g=lambda x,y:Lc[:,int(y*1000/gl),int(x*1000/gl)][:8].round(2)
  print(name,'Drax',g(5.77,3.69),'Wegsch',g(6.15,3.67),'Nase-S',g(5.2,3.3))
Hc=crop(H);Hr=M[int(r0):int(r1),int(c0):int(c1)][::2,::2]
D=dict(ny=Hc.shape[0],nx=Hc.shape[1],dx=dx,lny=Lc.shape[1],lnx=Lc.shape[2],lnz=len(AGL),ldz=25,ldx=gl,
 mny=Hr.shape[0],mnx=Hr.shape[1],mdx=6.434*2,h=enc(np.round(Hr*10),np.uint16),dirs=OUT)
json.dump(D,open('field3.json','w'));print(len(json.dumps(D))//1024,'KB',Hc.shape,Lc.shape)
