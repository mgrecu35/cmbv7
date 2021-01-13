#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "TKheaders.h"
#include "TK_2ADPR.h"
#include "TK_1CGMI.h"
TKINFO dprtkfile;
TKINFO       granuleHandle2AKu;
L2ADPR_SWATHS dprswath;
void openoutputfile_(char *jobname, char *fname);
int DayOfMonth[300], DayOfYear[300], Hour[300], MilliSecond[300],
  Minute[300], Month[300], Second[300], Year[300], SecondOfDay[300];
NAVIGATION navigation[300];
void open_dpr(char *dprfname)
{
  int status_alpha;
  char *jobname;
  jobname=(char*)malloc(sizeof(char)*30);
  sprintf(jobname,"junk");
  status_alpha = TKopen(dprfname,"2ADPR",TKREAD,"HDF5",jobname,&dprtkfile,1);
  printf("%i %s\n",status_alpha,dprfname);
}

int read_dpr(int iscan)
{
  int status=-1;
  status = TKseek(&dprtkfile, iscan, TK_ABS_SCAN_OFF);
  status=-1;
  if((TKendOfFile (&dprtkfile) != TK_EOF))
    {
      status=TKreadScan(&dprtkfile,&dprswath);
    }
  return status;
}

void process_scan(void)
{
  int j,k;
  float zKu[176], zKa[176];
  extern L2BCMB_SWATHS swath;
  int btop,bzd,bcf,bsfc;
  float srtPIAKu, dsrtPIA;
  int reliabFlagKu, reliabFlagDF;
  for(j=0;j<49;j++)
    {
      swath.NS.Latitude[j]=dprswath.NS.Latitude[j];
      swath.NS.Longitude[j]=dprswath.NS.Longitude[j];
      swath.NS.Input.precipitationType[j]=dprswath.NS.CSF.typePrecip[j];
      swath.NS.Input.surfaceElevation[j]=dprswath.NS.PRE.elevation[j];
      swath.NS.Input.localZenithAngle[j]=dprswath.NS.PRE.localZenithAngle[j];
      swath.NS.Input.surfaceType[j]=dprswath.NS.PRE.landSurfaceType[j];
      swath.NS.Input.surfaceRangeBin[j]=(dprswath.NS.PRE.binRealSurface[j]-1)/2;
      swath.NS.Input.stormTopBin[j]=(dprswath.NS.PRE.binStormTop[j]-1)/2; 
      if(swath.NS.Input.stormTopBin[j]<0)
	swath.NS.Input.stormTopBin[j]=-99;
      swath.NS.Input.stormTopAltitude[j]=dprswath.NS.PRE.heightStormTop[j];
      swath.NS.Input.lowestClutterFreeBin[j]=
	(dprswath.MS.PRE.binClutterFreeBottom[j] - 2)/2;
      srtPIAKu=dprswath.NS.SRT.PIAhybrid[j];
      reliabFlagKu=dprswath.NS.SRT.reliabFactorHY[j];
      if(dprswath.NS.PRE.flagPrecip[j]!=0)
	{
	  for(k=0;k<176;k++)
	    {
	      zKu[k]=dprswath.NS.PRE.zFactorMeasured[j][k];
	      if(j>=12 && j<37)
		zKa[k]=dprswath.MS.PRE.zFactorMeasured[j-12][k];
	      else
		zKa[k]=-99;
	    }
	}
    }
}
