      
	  
	  
	  subroutine vumat(
C Read only (unmodifiable)variables -
     1  nblock, ndir, nshr, nstatev, nfieldv, nprops, lanneal,
     2  stepTime, totalTime, dt, cmname, coordMp, charLength,
     3  props, density, strainInc, relSpinInc,
     4  tempOld, stretchOld, defgradOld, fieldOld,
     5  stressOld, stateOld, enerInternOld, enerInelasOld,
     6  tempNew, stretchNew, defgradNew, fieldNew,
C Write only (modifiable) variables -
     7  stressNew, stateNew, enerInternNew, enerInelasNew )
C
      include 'vaba_param.inc'
C
      dimension props(nprops), density(nblock), coordMp(nblock,*),
     1  charLength(nblock), strainInc(nblock,ndir+nshr),
     2  relSpinInc(nblock,nshr), tempOld(nblock),
     3  stretchOld(nblock,ndir+nshr),
     4  defgradOld(nblock,ndir+nshr+nshr),
     5  fieldOld(nblock,nfieldv), stressOld(nblock,ndir+nshr),
     6  stateOld(nblock,nstatev), enerInternOld(nblock),
     7  enerInelasOld(nblock), tempNew(nblock),
     8  stretchNew(nblock,ndir+nshr),
     8  defgradNew(nblock,ndir+nshr+nshr),
     9  fieldNew(nblock,nfieldv), stressNew(nblock,ndir+nshr), 
     +  stateNew(nblock,nstatev),enerInternNew(nblock), 
     +   enerInelasNew(nblock)
c
	  character*80 cmname
c	  
      real Unp,Us,Ymo,Ym,Ymf,Yms,D,maxD,Ymmax,one
 	  real Gtc,Betas,Unn
	  dimension U(6),sig(6)
	  integer km,i
      parameter (one=1)
c 	  
      Knp=PROPS(1)
	  Knn=PROPS(2)
	  Ks=PROPS(3)
	  GcI=PROPS(4)
      GcII=PROPS(5)
	  GoI=PROPS(6)
	  GoII=PROPS(7)
	  AlphaI=PROPS(8)
	  BetaI=PROPS(9)
C	 
	  Do Km=1,nblock

      if ((stepTime.eq.0).AND.(totalTime.eq.0)) then
      do i=1,6
	        sig(i)=0
	  enddo
c	  
		if (strainInc(km,1).eq.0) then
		Unp=0
		Unn=0
		else if (strainInc(km,1).lt.0) then
		Unp=strainInc(km,1)
		Unn=0
		else
		Unn=strainInc(km,1)
		Unp=0
		end if
c
      sig(1)=Knp*Unp+Knn*Unn
	  sig(2)=Ks*strainInc(km,2)*2
      sig(3)=Ks*strainInc(km,3)*2
c      
	  stressNew(km,1)=sig(1)
      stressNew(km,2)=sig(2)
	  stressNew(km,3)=sig(3)
	  stressNew(km,4)=sig(4)
	  stressNew(km,5)=sig(5)
      stressNew(km,6)=sig(6)
c
c	  
	  stateNew(km,1)=0
      stateNew(km,2)=0
	  stateNew(km,3)=0
c
	  D=0
	  stateNew(km,12)=D
      maxD=0
c
	goto  8888 
	end if
	  
c    Calculate new displacement
c 
      U(1)=stateOld(km,4)+strainInc(km,1)
	  if (stateOld(km,12).eq.1) then
	  U(2)=stateOld(km,5)
	  U(3)=stateOld(km,6)
	  else
	  U(2)=stateOld(km,5)+strainInc(km,2)*2
	  U(3)=stateOld(km,6)+strainInc(km,3)*2
	  end if 
c
	  Unp=0
	  Unn=0
c	  
		if (U(1).lt.0) then
			if (stateOld(km,12).eq.1) then
			Unp=stateOld(km,4)
			else
			Unp=U(1)
			end if
		U(1)=Unp
		Unn=0
		else
		Unn=U(1)
		Unp=0		
		end if 
c	  
	  Us=abs(sqrt(U(2)**2+U(3)**2))
c	  
	  do i=1,6
	  sig(i)=0
	  enddo
c	  
      if (Unp.eq.0) then
	  Ymo=GoII
	  Gtc=GcII
	  else
	  Betas=(ks/Knp)*((Us/Unp)**2)
	  Ymo=(1+betas)*GoI*GoII/(GoII**AlphaI+(betas*GoI)**AlphaI)**(1/AlphaI)
      Gtc=(1+betas)*GcI*GcII/(GcII**BetaI+(betas*GcI)**BetaI)**(1/BetaI)
	  end if
c
      Ymf=Gtc	
c	  	 
      Ym=0.5*knp*Unp**2+0.5*ks*Us**2
c	  
 	  if (Ym.gt.Ymo) then
      D=abs((1/(Ymo-Ymf))*(sqrt((Ymo*Ymf**2)/Ym)-Ymf))
      else
      D=0
      end if
c	  
 	  maxD=max(stateold(km,12),D)
c
      D=min(one,maxD)
c	  if (D.eq.1) then
c	  stateNew(km,10)=0
c	  end if 
c	  
 	  sig(1)=(1-D)*knp*Unp+knn*Unn
	  sig(2)=(1-D)*ks*U(2)
      sig(3)=(1-D)*ks*U(3)
c	  
	  stressNew(km,1)=sig(1)
      stressNew(km,2)=sig(2)
	  stressNew(km,3)=sig(3)
	  stressNew(km,4)=sig(4)
	  stressNew(km,5)=sig(5)	
	  stressNew(km,6)=sig(6)
c
	  stateNew(km,1)=0
      stateNew(km,2)=0
	  stateNew(km,3)=0
c	
	  stateNew(km,4)=U(1)
	  stateNew(km,5)=U(2)
	  stateNew(km,6)=U(3)
	  stateNew(km,7)=U(4)
	  stateNew(km,8)=U(5)
	  stateNew(km,9)=U(6)
	  stateNew(km,12)=D


c	  
 8888 CONTINUE     
	End do

      return 
      end
