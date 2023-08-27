# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:36:11 2022

@author: Steven
"""
import numpy as np 

import matplotlib.pyplot as plt
import matplotlib.tri as mtri








def Boundary(elt,vtx):
   s = []
   for k in range(len(elt)):
           s.append(tuple(sorted([elt[k][0],elt[k][1]])))
           s.append(tuple(sorted([elt[k][1],elt[k][2]])))
           s.append(tuple(sorted([elt[k][2],elt[k][0]])))
   eltb = []
   #valeur a enlever
   Lx = [-1.0,1.0]
   Ly = [-0.5,0.5]
   
   #retire les doublons
   for k in s:
       if ((k[1],k[0]) in s  ):
          
        
           s.remove(k)
        
   #gere les bords
   for i in s:
       n=0
       for j in elt:
           if(i[0] in j and i[1] in j ):
               n = n + 1
       if(n==1 ):
           eltb.append(i)
           
   eltb0 = [] 
   #compute Omega0
   for k in eltb:
       for j in k :
           if(vtx[j][0] not in Lx and vtx[j][1] not in Ly ):
               eltb0.append(k)
               
   I = set(eltb0)
   eltb0 = list(I);
   

           
    
    
   return eltb0



def LoadVTX(nom_fichier):
    data = open(nom_fichier,"r")
    L=[]
    for ligne in data:
         L.append(ligne)
    
    R = L[L.index('$Noeuds\n')+2:L.index('$FinNoeuds\n')]
    
    for i in range(len(R)):
        R[i]=R[i].split()
        R[i].pop(0)
        for j in range(len(R[i])):
            R[i][j]=float(R[i][j])
            
        
    data.close()
    return R

def LoadELT(nom_fichier):
    data = open(nom_fichier,"r")
    L=[]
    for ligne in data:
         L.append(ligne)
    
   
    R = L[L.index('$Elements\n')+2:L.index('$FinElements\n')]
    Label = []
   
    for i in range(len(R)):
        R[i]=R[i].split()
        R[i].pop(0)
        Label.append(int(R[i][3]))
        R[i].pop(3)
        for j in range(len(R[i])):
            R[i][j]=int(R[i][j])
            
    
    return R,Label
     
def Mloc(vtx, e):
    
    if len(e)==3 : 
        s0 = np.array(vtx[e[0]]) 
        s1 = np.array(vtx[e[1]])
        s2 = np.array(vtx[e[2]])
        a = np.linalg.norm(s1-s0)
        b = np.linalg.norm(s2-s1)
        c = np.linalg.norm(s2-s0)
    
        d = (a+b+c)/2
        aire = np.sqrt((d*(d-a)*(d-b)*(d-c)))
    
        M = 2*np.eye(3,3) +1*np.eye(3,3,1)+1*np.eye(3,3,-1)
        M[2,0]=1
        M[0,2]=1
        M *= aire/12
        
        return M
    else :
        s0 = np.array(vtx[e[0]]) 
        s1 = np.array(vtx[e[1]])
        y = np.linalg.norm(s1-s0)
        M = 2*np.eye(2,2) +np.eye(2,2,1)+np.eye(2,2,-1)

        
        M *= y/6
        return M
def rigiditeloc(vtx,e):
    s0 = np.array(vtx[e[0]]) 
    s1 = np.array(vtx[e[1]])
    s2 = np.array(vtx[e[2]])
    a = np.linalg.norm(s1-s0)
    b = np.linalg.norm(s2-s1)
    c = np.linalg.norm(s2-s0)

    d = (a+b+c)/2
    aire = np.sqrt((d*(d-a)*(d-b)*(d-c)))
    K = np.zeros((3,3))
    
    for j in range(3):
        for k in range(3):
            sj = np.array(vtx[e[(j+2)%3]]) - np.array(vtx[e[(j+1)%3]])
            sk = np.array(vtx[e[(k+2)%3]]) - np.array(vtx[e[(k+1)%3]])
            K[k,j]=np.dot(sj,sk)
    K /= 4*aire 
    
    return K 


def Mass(vtx,elt):
    
    Masse = np.zeros((len(vtx),len(vtx)))
    Mbound = np.zeros((len(vtx),len(vtx)))
    Rigidite = np.zeros((len(vtx),len(vtx)))
    w0 = sorted(Boundary(elt[0],vtx))
  
    for q in range(len(elt[0])):
        for l in range(3):
            for m in range(3):
                j = elt[0][q][l]
                k = elt[0][q][m]
                if elt[1][q] == 2 :
                    Masse[j,k] += Mloc(vtx,elt[0][q])[l,m]
                Rigidite[j,k] += rigiditeloc(vtx,elt[0][q])[l,m]
  
    for q in range(len(w0)):
        
        for l in range(2):
            for m in range(2):
                j = w0[q][l]
                k = w0[q][m]
                Mbound[k,j] += Mloc(vtx,w0[q])[l,m]
    
    
    
    # test sur la masse :
    U = np.ones(np.shape(Masse)[0]).transpose()
    print(np.dot(np.dot(U, Masse), U))
    
 

                
   
    return (Rigidite+Mbound+Masse)
                
  
def F(vtx,elt):
    label = elt[1]
    elements  = elt[0]
    w0 = sorted(Boundary(elements,vtx))
    f = np.zeros((len(vtx),1))
    
    
    
    
    
    for q in range(len(elements)):
        for l in range(3):
            if label[q]==2:
                
                
                j = elements[q][l]
                s0 = np.array(vtx[elements[q][0]]) 
                s1 = np.array(vtx[elements[q][1]])
                s2 = np.array(vtx[elements[q][2]])
                a = np.linalg.norm(s1-s0)
                b = np.linalg.norm(s2-s1)
                c = np.linalg.norm(s2-s0)

                d = (a+b+c)/2
                aire = np.sqrt((d*(d-a)*(d-b)*(d-c)))
               
                f[j] += (1/3)*aire 
    for q in range(len(w0)):
        
        for l in range(2):
            j = w0[q][l]
            s0 = np.array(vtx[w0[q][0]]) #sj
            s0 = np.append(s0,0)
            s1 = np.array(vtx[w0[q][1]]) #sj+1
            s1 = np.append(s1,0)
            a = np.linalg.norm(s1-s0)
           
     
            f[j] += a/2
          
            

            
            

  
    return f




def Mass2(vtx,elt):
    
    Masse = np.zeros((len(vtx),len(vtx)))
    Mbound = np.zeros((len(vtx),len(vtx)))
    Rigidite = np.zeros((len(vtx),len(vtx)))
    w0 = sorted(Boundary(elt[0],vtx))
  
    for q in range(len(elt[0])):
        for l in range(3):
            for m in range(3):
                j = elt[0][q][l]
                k = elt[0][q][m]
                
                Masse[j,k] += Mloc(vtx,elt[0][q])[l,m]
                Rigidite[j,k] += rigiditeloc(vtx,elt[0][q])[l,m]
  
    for q in range(len(w0)):
        
        for l in range(2):
            for m in range(2):
                j = w0[q][l]
                k = w0[q][m]
                Mbound[k,j] += Mloc(vtx,w0[q])[l,m]
    
    
    
    # test sur la masse :
    U = np.ones(np.shape(Masse)[0]).transpose()
    print(np.dot(np.dot(U, Masse), U))
        
 
    

                
   
    return (Rigidite+Mbound+Masse)

def F2(vtx,elt):
    label = elt[1]
    elements  = elt[0]
    f = np.zeros((len(vtx),1))
 
    

    for q in range(len(elements)):
        for l in range(3):
            if label[q]==2:
                
                
                j = elements[q][l]
                s0 = np.array(vtx[elements[q][0]]) 
                s1 = np.array(vtx[elements[q][1]])
                s2 = np.array(vtx[elements[q][2]])
                a = np.linalg.norm(s1-s0)
                b = np.linalg.norm(s2-s1)
                c = np.linalg.norm(s2-s0)

                d = (a+b+c)/2
                aire = np.sqrt((d*(d-a)*(d-b)*(d-c)))
               
                f[j] += (1/3)*aire 

  
    return f

    
vtx  = LoadVTX("config2.msh")
elt = LoadELT("config2.msh")
A = Mass2(vtx,elt)
f = F2(vtx,elt)

solution1=np.linalg.solve(A,f)





def PlotSubDomain(vtx,elt,label):
    bord = Boundary(elt,vtx)
    for i in bord:
        x_cord = []
        y_cord = []
        
        x_cord.append(vtx[i[0]][0])
        x_cord.append(vtx[i[1]][0])
        y_cord.append(vtx[i[0]][1])
        y_cord.append(vtx[i[1]][1])
        
        plt.plot(x_cord,y_cord,"blue")
    
    #il faut faire la triangulation en fonction de label
    
    x =[]
    y = []
    for i in range(len(vtx)):
        x.append(vtx[i][0])
        y.append(vtx[i][1])
    
    elt1 = [elt[i] for i in range(len(elt)) if label[i]==1]  
    elt2 = [elt[i] for i in range(len(elt)) if label[i]==2]
    triang = mtri.Triangulation(x, y, elt1)
    triang2 = mtri.Triangulation(x, y, elt2)
    triang3 = mtri.Triangulation(x,y,elt)
    
    res = []
    for k in range(len(vtx))  :
       res.append([vtx[k][0], vtx[k][1]])
       
    #afficher la solution sur le domaine a decommenter ou pas 
    
    val = []
    for i in range(len(res)) :
        val.append(solution1[i][0])
        
    #print(np.linalg.norm(val,2))
   
    "on obtient une norme L2 de l'rodre l a 2.78e-14  pour config 1 et 1.e-12 pour config 2"

    
   
 
    t=plt.tricontourf(triang3, np.array(val))
    plt.triplot(triang,'b-')
    plt.triplot(triang2,'r-')
    plt.colorbar(t) 
   
    plt.title("Uh for config 1")
    plt.show()
    
    
    
    return  






    
PlotSubDomain(vtx,elt[0],elt[1])




