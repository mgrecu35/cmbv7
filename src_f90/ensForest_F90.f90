
subroutine ensForest_Nw(zku,zka,Nw,dm_out,n)
use tablep2
integer :: i, n, ibin
real :: dm(5), dm_m
real :: zku(n), zka(n)
real, intent(out) :: nw(n),dm_out(n)
do i=1,n
    if(zku(i)<10) zku(i)=0
    if(zka(i)<10) zka(i)=0
    call treeReg_dm_0(zku(i),zka(i),dm(1))
    call treeReg_dm_1(zku(i),zka(i),dm(2))
    call treeReg_dm_2(zku(i),zka(i),dm(3))
    call treeReg_dm_3(zku(i),zka(i),dm(4))
    call treeReg_dm_4(zku(i),zka(i),dm(5))
    dm_m=sum(dm(1:5))/5
    dm_out(i)=dm_m
    call bisection2(dms(1:253),253,dm_m,ibin)
    nw(i)=(zku(i)-zkus(ibin))/10.0
enddo
end subroutine ensForest_Nw