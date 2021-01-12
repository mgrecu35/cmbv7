/* All rights to software held by NASA/GSFC PPS */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "TKheaders.h"
#include "TK_1CGMI.h"

void pymain_(void){

TKINFO *newtkfileinfo;
L1CGMI_SWATHS *swaths;
int i,ic,ret;

char *writefile="./L1CGMI.HDF5";

swaths=(L1CGMI_SWATHS*)malloc(sizeof(L1CGMI_SWATHS));
newtkfileinfo=(TKINFO*)malloc(sizeof(TKINFO));

ret=TKopen(writefile,"1CGMI",TKWRITE,"HDF5","jobid",newtkfileinfo,1);
printf("TKopen %d\n",ret);

for(i=0; i<3000; i++)
{

    swaths->S1.ScanTime.Hour = 1;
    swaths->S1.ScanTime.Minute = 1;
    swaths->S1.ScanTime.Second = 1;

    swaths->S2.ScanTime.Hour = 2;
    swaths->S2.ScanTime.Minute = 2;
    swaths->S2.ScanTime.Second = 3;

    for (ic=0; ic < 221; ic++)
    {
        swaths->S1.Latitude[ic] = 1;
        swaths->S2.Latitude[ic] = 2;
    }

    ret=TKwriteScan(newtkfileinfo,swaths);
    if ((i%1000)==0) printf("TKwriteScan %d\n",ret);
    if (ret < 0)
    {
        printf("TKwriteScan return %d\n",ret);
        ret=TKclose(newtkfileinfo);
        printf("TKclose return %d\n",ret);
        exit(-1);
    }

}

ret=TKclose(newtkfileinfo);
printf("TKclose %d\n",ret);

free(swaths);
free(newtkfileinfo);


} 
