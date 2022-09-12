module tableP2
  real :: zKuSJ(300)
  real :: zKudN(300)
  real :: zKaSJ(300)
  real :: dNT(300)
  real :: dmJ(300)
  real :: rJ(300)
  real :: logRJ(300)
  real :: attKaJ(300)
  real :: attKuJ(300)
  integer :: nJ
end module tableP2
subroutine initP2
  use tableP2
  use tables2
  implicit none
  integer :: i
  real :: f
  f=1
  do i=1,nbins
     zKuSJ(i)=zmin+(i-1)*dzbin
     zKaSJ(i)=z35Table(i,1)
     dmJ(i)=d013Table(i,1)
     attKaJ(i)=att35Table(i,1)
     attKuJ(i)=att13Table(i,1)
     rJ(i)=pr13Table(i,1)
     logRJ(i)=log10(pr13Table(i,1))
     if(dmj(i).lt.0.8) then
        dnT(i)=1.5*log((0.8/dmj(i))**0.25)+0.0
     else
        dnT(i)=1.0*log((0.8/dmj(i))**0.25)+0.0
     end if
     zKudN(i)=zKuSJ(i)+10*dnT(i)
  end do
  !print*,f
  !stop
  nJ=nbins
  !print*, d013Table(200:240,1),nbins,nbinS2,nbinH
end subroutine initP2

