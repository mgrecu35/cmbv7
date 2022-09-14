!void fModelFortran(float *z13obs, float *z35obs, 
!		   int nodes[5], int isurf, int imu,
!		   float *log10dNP, int *nodeP, int nNodes, 
!		   float *pia35M, float *pia13M,
!		   float *z35mod, float *pwc, float dr, int ic, int jc, 
!		   float *hh,
!		   float delta, int iNode, int nmfreq, 
!		   float *salb, float *kext,float *asym, int itype,
!		   int ngates,float *rrate,float *d0,float *log10dN,
!		   float *z13, float *z35,
!		   int *imuv, float *hfreez,float *dz, 
!		   float *pia13srt, float *relPia13srt,
!		   float *pia35srt, float *relPia35srt,
!//  SFM  begin  06/22/2014; for M.Grecu  (unknown justification)
!//  SFM  begin  07/01/2014; for M.Grecu  random sequences
!		   int *imemb,float *localZAngle, float *wfractPix, 
!		   float *xs, long *ichunk, float nstdA)
!//  SFM  end    07/01/2014
!//  SFM  end    06/22/2014
subroutine interpol(xn,yn,n,fint)
  implicit none
  integer :: n,xn(n)
  real :: yn(n), fint(88)
  integer :: i,n1
  real :: f
  fint=0
  do i=1,n-1
     do n1=xn(i),min(xn(i+1),88)
        f=(n1-xn(i))/(xn(i+1)-xn(i)+1e-3)
        fint(n1)=(1-f)*yn(i)+f*yn(i+1)
     end do
  end do
end subroutine interpol

subroutine fmodel_fortran(z13obs,z35obs,node,isurf,imu,log10dnP,nodeP,nNodes,&
     pia35m,pia13m,z35mod,pwc,dr,ic,jc,hh,nmfreq,salb,kext,asym,&
     itype,ngates,rrate,dm,log10dn,z13,z35,hfreez,pia13srt,relpia13srt,&
     pia35srt,relpia35srt,imemb,xs,nstdA,log10dn_in)
  implicit none
  integer :: ngates, imemb,ithresh
  real :: log10dnP(nNodes)
  integer :: nodeP(nNodes),nNodes
  real, intent(out) :: pia35m,pia13m,z35mod(ngates),pwc(ngates)
  real :: log10dn_in(ngates)
  real :: dr,ic,jc,hh(ngates)
  integer :: nmfreq
  real, intent(out) :: salb(ngates,nmfreq),kext(ngates,nmfreq),asym(ngates,nmfreq)
  integer ::  itype, ifreq
  real,intent(out) :: rrate(ngates),dm(ngates)
  real,intent(out) :: log10dn(ngates)
  real :: hfreez
  real :: pia13srt,pia35srt
  integer :: relpia35srt,relpia13srt
  real :: z13obs(ngates), z35obs(ngates)
  integer :: node(5), isurf, imuv(ngates), imu
  integer ::  iLev, i, i1, i2
  real ::  att1,att351,dndum,z351
  real ::  fi, fi1, log10dNPi, f, ntot
  real ::  atm_extKav,cld_extKav,att35,att13,z13obsP(88)
  integer :: nSub
  integer :: countSub(88)
  real :: kextSub(88,8,50),salbSub(88,8,50),asymSub(88,8,50), &
       kextAvg(88,8), salbAvg(88,8), asymAvg(88,8), rainAvg(88), pwcAvg(88), &
       dmAvg(88), rrateSub(88,50), pwcSub(88,50), dmSub(88,50), &
       z35modSub(88,50), z35Sub(88,50), z13Sub(88,50), pia35Sub(50), &
       pia13Sub(50)
   real, intent(out) :: z13(ngates),z35(ngates)

  real ::  z13sfc, z13sfcA, z35sfc, z35sfcA;
  real ::  pia13tot, pia35tot
  real ::  l_13(ngates), l_35(ngates)
  integer :: j,freq
  integer :: iSub
  real :: tau
  integer :: count
  real  :: nstd, sxs, xs(50), nstdA
  
  pia13tot=0
  pia35tot=0
  nsub=7

  nstd=nstdA
  nSub=8
  ithresh=0
  sxs=0
  do i=1,nsub
     xs(i)=exp(nstd*xs(i)) 
     sxs=sxs+xs(i)
  enddo
  
  sxs=sxs/nSub
  do i=1,nsub
     xs(i)=xs(i)/sxs
     xs(i)=10.*log10(xs(i));
  enddo
  
  log10dN=-99.9
  dm=0
  rrate=0
  z13obsP=-99

  pia35M=0
  pia13M=0

  
  imuv=imu
  !print*, nodeP
  !return
  call interpol(nodeP,log10dnP,nNodes,log10dn)
  !print*,log10dn_in
  do i=node(1),node(5)
   if (log10dn_in(i)>-99.9) then
      log10dn(i)=log10dn(i)+log10dn_in(i)
      !print*, log10dn(i), log10dn_in(i)
   end if
  end do
  !print*,node(1),node(5)
  !print*, log10dnp
  !return 
  z13=z13obs
  z13obsP=z13obs

  rrateSub=-99.
  dmSub=-99.
  pwcSub=-99.
  z35modSub=-99.
  z35Sub=-99.
  z13Sub=-99.
  kextSub=-99.
  salbSub=-99.
  asymSub=-99.
  kextAvg=0.
  salbAvg=0.
  asymAvg=0.
  z13sfc=0
  z13sfcA=0
  z35sfc=0
  z35sfcA=0
  do i=1,nsub
     do j=node(1),node(5)
        z13obsP(j)= z13obs(j)+xs(i)
        if(z13obsP(j)>50) z13obsP(j)=50
     enddo
     !print*,i,'before fhb'
     call fhb12(z13,z35,z13obsP, &
          pia13M,pia35M,z35mod,pwc,log10dN, &
          dr,node,isurf,imuv, &
          ngates,nmfreq,hh,itype,kext,salb,asym, &
          rrate,dm,hfreez, pia13srt)
      !print*,i,'after fhb'
      if(z13obs(node(5))>12) then
         z13sfc=z13sfc+10**(0.1*z13(node(5)))
         z13sfcA=z13sfcA+10**(0.1*z13(node(5))-0.1*(pia13M))
         z35sfc=z35sfc+10**(0.1*z35(node(5)));
         z35sfcA=z35sfcA+10**(0.1*z35(node(5))-0.1*(pia35M))
         ithresh=ithresh+1
      endif
      ic=0
      pia13tot=pia13tot+pia13M
      pia35tot=pia35tot+pia35M
      l_13(i)=10**(-0.1*(pia13M))
      l_35(i)=10**(-0.1*(pia35M))

      
      kextSub(:,:,i)=kext
      salbSub(:,:,i)=salb
      asymSub(:,:,i)=asym

      tau=0
      do j=1,88
         rrateSub(j,i)=rrate(j)
         dmSub(j,i)=dm(j)
         pwcSub(j,i)=pwc(j)
         if(salbSub(j,4,i)>0 .and. kextSub(j,4,i)>0) then
            tau=tau+salbSub(j,4,i)*kextSub(j,4,i)*0.25;
            !z35mod(j)=z35mod(j)+tau*7
            z35modSub(j,i)=z35mod(j)
            z35Sub(j,i)=z35(j)
            z13Sub(j,i)=z13(j)
         endif
      enddo
         

      
      countSub=0
      rrate=0.
      pwc=0
      dm=0.
      z35=0
      z35mod=0
      z13=0
   end do
   !return
   do i=node(1),node(5)
      if(z13obs(i)>12) then
         do isub=1,nSub
            if(kextSub(i,1,iSub)>0) then
               z35mod(i)=z35mod(i)+10**(0.1*z35modSub(i,iSub))
               z13(i)=z13(i)+10**(0.1*z13Sub(i,iSub))
               z35(i)=z35(i)+10**(0.1*z35Sub(i,iSub))
               rrate(i)=rrate(i)+rrateSub(i,iSub)
               pwc(i)=pwc(i)+pwcSub(i,iSub)
               dm(i)=dm(i)+dmSub(i,iSub)
               countSub(i)=countSub(i)+1
            endif
         enddo
      endif
   enddo
   
   !print*, 'aggregation'
   if(ithresh>0) then
      if(z13sfcA>0.01 .and. z13sfc>0.01) then
         pia13M=log10(z13sfc/z13sfcA)*10.0
      else
         pia13M=pia13tot/nSub
      endif
      if(z35sfcA>0.01 .and. z35sfc>0.01) then
         pia35M=log10(z35sfc/z35sfcA)*10.
      else
         pia35M=pia35tot/nSub
      endif
   else
      pia13M=pia13tot/nSub;
      pia35M=pia35tot/nSub;
   endif
   !print*, pia13M, pia35M
   do i=node(1),node(5)
      if(countSub(i)>0) then
         z35mod(i)=10.*log10(z35mod(i)/countSub(i));
         z13(i)=10.*log10(z13(i)/countSub(i));
         z35(i)=10.*log10(z35(i)/countSub(i));
         rrate(i)=rrate(i)/countSub(i);
         pwc(i)=(pwc(i)/countSub(i));
         dm(i)=dm(i)/countSub(i);
      else
         z35mod(i)=-99;
         z13(i)=-99;
         z35(i)=-99;
         rrate(i)=-99;
         pwc(i)=-99;
      endif
   enddo
   !return 
   do i=1,nNodes
      log10dNP(i)=log10dN(nodeP(i));
   end do


   do j=1,88
      do ifreq=1,8
         count=0
         kextAvg(j,ifreq)=0
         salbAvg(j,ifreq)=0
         asymAvg(j,ifreq)=0
         do isub=1,nSub
            if(kextSub(j,ifreq,iSub)>0) then
               kextAvg(j,ifreq)=kextAvg(j,ifreq)+kextSub(j,ifreq,iSub)
               salbAvg(j,ifreq)=salbAvg(j,ifreq)+salbSub(j,ifreq,iSub)
               asymAvg(j,ifreq)=asymAvg(j,ifreq)+asymSub(j,ifreq,iSub)
               count=count+1;
            endif
         enddo
         if(count>0) then
            kextAvg(j,ifreq)=kextAvg(j,ifreq)/count;
            salbAvg(j,ifreq)=salbAvg(j,ifreq)/count;
            asymAvg(j,ifreq)=asymAvg(j,ifreq)/count;
         else
            kextAvg(j,ifreq)=-99;
            salbAvg(j,ifreq)=-99;
            asymAvg(j,ifreq)=-99;
         endif
      end do
   end do
   ic=0

   
   kext=kextAvg
   salb=salbAvg
   asym=asymAvg
   !print*, (l_35)
   pia13M=-10.*log10(sum(l_13(1:nsub))/nSub)
   pia35M=-10.*log10(sum(l_35(1:nsub))/nSub)

   

   !if(isinf(pia35M)) then
   !   pia35M=pia35tot/nSub
   !endif
     
   do j=1,88
      if(log10dN(j)>4.5) log10dN(j)=4.5
      if(log10dN(j)<-4.5) log10dN(j)=-4.5
   enddo
 end subroutine fmodel_fortran
 
