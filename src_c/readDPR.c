#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "TKheaders.h"
#include "TK_2ADPR.h"
#include "TK_1CGMI.h"
#include <math.h>

TKINFO dprtkfile;
TKINFO       granuleHandle2AKu;
L2ADPR_SWATHS dprswath;
L2ADPRX_SWATHS dprswathx;
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

void open_dprx(char *dprfname)
{
  int status_alpha;
  char *jobname;
  jobname=(char*)malloc(sizeof(char)*30);
  sprintf(jobname,"junk");
  status_alpha = TKopen(dprfname,"2ADPRX",TKREAD,"HDF5",jobname,&dprtkfile,1);
  printf("%i %s\n",status_alpha,dprfname);
}

int read_dprx(int iscan)
{
  int status=-1;
  status = TKseek(&dprtkfile, iscan, TK_ABS_SCAN_OFF);
  status=-1;
  if((TKendOfFile (&dprtkfile) != TK_EOF))
    {
      status=TKreadScan(&dprtkfile,&dprswathx);
    }
  return status;
}

void convretf90_(float *rrate,float *dmOut,float *dm_sub,float *rrate_sub,
		 int *bzd,int *bcf,float *piaka_sub,float *piahb_sub,
		 float *piaSRTKu,float *dpiaSRT,int *relFlagKu,int *relFlag,float *zetaS);
  
void convective(int btop,int bzd,int bcf,int bsfc, float *zKu, float *zKa,
		float piaSRTKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa, int sfcType);

void stratiform(int btop,int bzd,int bcf,int bsfc, int binBB, int binBBT, float *zKu, float *zKa,
		float srtPIAKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa);
void process_scan(void)
{
  int j,k;
  float zKu[176], zKa[176];
  extern L2BCMB_SWATHS swath;
  int btop,bzd,bcf,bsfc,binBBT, binBB;
  float srtPIAKu, dsrtPIA;
  int reliabFlagKu, reliabFlagDF;
  int nodes5[5];
  float pRate[176],dn[176], dm[176];
  float piaKu, piaKa;
  int sfcType;
  for(j=0;j<49;j++)
    {
      swath.NS.Latitude[j]=dprswath.NS.Latitude[j];
      swath.NS.Longitude[j]=dprswath.NS.Longitude[j];
      swath.NS.Input.precipitationType[j]=dprswath.NS.CSF.typePrecip[j];
      swath.NS.Input.surfaceElevation[j]=dprswath.NS.PRE.elevation[j];
      swath.NS.Input.localZenithAngle[j]=dprswath.NS.PRE.localZenithAngle[j];
      swath.NS.Input.surfaceType[j]=dprswath.NS.PRE.landSurfaceType[j];
      sfcType=dprswath.NS.PRE.landSurfaceType[j];
      swath.NS.Input.surfaceRangeBin[j]=(dprswath.NS.PRE.binRealSurface[j]-1)/2;
      swath.NS.Input.stormTopBin[j]=(dprswath.NS.PRE.binStormTop[j]-1)/2;
      btop=dprswath.NS.PRE.binStormTop[j];
      binBB=dprswath.NS.CSF.binBBPeak[j];
      binBBT=dprswath.NS.CSF.binBBTop[j];
      bcf=dprswath.NS.PRE.binClutterFreeBottom[j];
      bzd=dprswath.NS.VER.binZeroDeg[j];
      bsfc=dprswath.NS.PRE.binRealSurface[j];
      if(swath.NS.Input.stormTopBin[j]<0)
	swath.NS.Input.stormTopBin[j]=-99;
      swath.NS.Input.stormTopAltitude[j]=dprswath.NS.PRE.heightStormTop[j];
      swath.NS.Input.lowestClutterFreeBin[j]=
	(dprswath.MS.PRE.binClutterFreeBottom[j] - 2)/2;
      srtPIAKu=dprswath.NS.SRT.PIAhybrid[j];
      reliabFlagKu=dprswath.NS.SRT.reliabFactorHY[j];
      if(dprswath.NS.PRE.flagPrecip[j]==0)
	swath.NS.surfPrecipTotRate[j]=0;
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
	   if((int)(dprswath.NS.CSF.typePrecip[j]/1e7)==2)
	     {
	       if(reliabFlagKu==2)
		 reliabFlagKu=1;
	       float piadSRT=5*srtPIAKu;
	       int reliabFlag=reliabFlagKu;
	       reliabFlagKu=-1;
	       convective(btop,bzd,bcf,bsfc,zKu,zKa,
			  srtPIAKu,reliabFlagKu, piadSRT, reliabFlag,
			  nodes5, pRate,
			  dn, dm, &piaKu, &piaKa, sfcType);
	       swath.NS.surfPrecipTotRate[j]=pRate[bcf];
	       swath.NS.surfPrecipTotRate[j]=pRate[bcf];
	       swath.NS.phaseBinNodes[j][4]=(int)(bsfc/2);
	       swath.NS.phaseBinNodes[j][0]=(int)(btop/2);
	       swath.NS.phaseBinNodes[j][2]=(int)(bzd/2);
	       for(k=0;k<btop;k=k+2)
		 {
		   int k2=(int)(k/2);
		   swath.NS.precipTotRate[j][k2]=0;
		 }
	       for(k=btop;k<bcf;k=k+2)
		 {
		   int k2=(int)(k/2);
		   swath.NS.precipTotRate[j][k2]=pRate[k];
		   swath.NS.precipTotPSDparamHigh[j][k2]=dm[k];
		 }
	       //
	       if(pRate[bcf]>300 || pRate[bcf]<0)
		 {
		   printf("%i %g %g %g %i\n",j,pRate[bcf],srtPIAKu,zKu[bcf],
			  bcf);
		   exit(0);
		 }

	       if(isnan(pRate[bcf]))
		 {
		   printf("%i %g %g %g %i\n",j,pRate[bcf],srtPIAKu,zKu[bcf],bcf);
		   exit(0);
		 }
	     }
	   else
	     swath.NS.surfPrecipTotRate[j]=0;
	   if((int)(dprswath.NS.CSF.typePrecip[j]/1e7)==1)
	     {
	       if(reliabFlagKu==2)
		 reliabFlagKu=1;
	       float piadSRT=5*srtPIAKu;
	       int reliabFlag=reliabFlagKu;
	       reliabFlagKu=-1;
	       stratiform(btop,bzd,bcf,bsfc,binBB,binBBT,zKu,zKa,
			  srtPIAKu, reliabFlagKu, piadSRT, reliabFlag,
			  nodes5, pRate, dn, dm, &piaKu, &piaKa);
	       if(pRate[bcf]<0)
		 {
		   for(k=bzd;k<=bcf;k++)
		     printf("%g %g",pRate[k],zKu[k]);
		   printf("\n");
		   exit(0);
		 }
	       swath.NS.surfPrecipTotRate[j]=pRate[bcf];
	       swath.NS.phaseBinNodes[j][4]=(int)(bsfc/2);
	       swath.NS.phaseBinNodes[j][0]=(int)(btop/2);
	       swath.NS.phaseBinNodes[j][2]=(int)(bzd/2);
	       for(k=0;k<btop;k=k+2)
		 {
		   int k2=(int)(k/2);
		   swath.NS.precipTotRate[j][k2]=0;
		 }
	       for(k=btop;k<bcf;k=k+2)
		 {
		   int k2=(int)(k/2);
		   swath.NS.precipTotRate[j][k2]=pRate[k];
		   swath.NS.precipTotPSDparamHigh[j][k2]=dm[k];
		 }
	       //
	       //if(!(binBB>0))
	       // printf("%g %g %g %g\n",piaKu,piaKa,pRate[bcf],zKu[bcf]);
	       //printf("%g %g %g\n",piaKu,piaKa,pRate[bcf]);
	     }
	  
	     
	}
    }
}

void iter_profcv2_(int *btop,int *bzd,int *bcf,int *bsfc,float *zKuL,
		   float *zKaL,float *dr,int *n1d,float *eps,int *imu,
		   float *dn1d,float *dm1d,float *rrate1d,float *zKuC,
		   float *zKaSim,float *epst,float *piaKu,float *piaKa,
		   int *itype,float *dncv,float *dnp,float *dzdn, 
		   float *piaSRTKu,int *relPIASRTKu,
		   float *rrate1d_sub, float *dn_sub,
		   float *dm_sub, float *zkuc_sub, float *piahb_sub,
		   float *piaKa_sub,float *zetaS,float *piaKuS,float *piaKaS);
  
void convective(int btop,int bzd,int bcf,int bsfc, float *zKu, float *zKa,
		float srtPIAKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa, int sfcType)
{
  float dr=0.125, dncv=0.0, eps=1.0, epst;
  int imu=3, itype=2, n1d=176;
  float zKuC[176], zKaSim[176], rrate1d_sub[176*31],dn_sub[176*31],
    dm_sub[176*31], zkuc_sub[176*31], piahb_sub[31], piaKa_sub[31],
    zetaS[31], dzdn[176*176], dnp[176];
  int i;
  float piaKuS,piaKaS;
  for(i=0;i<176;i++)
    dnp[i]=0;
  if(sfcType==0)
    dncv=0.1;
  //printf("%i ",bzd);
  iter_profcv2_(&btop,&bzd,&bcf,&bsfc,zKu,
		zKa,&dr,&n1d,&eps,&imu,dn,dm,pRate,zKuC,
		zKaSim,&epst,piaKu,piaKa,
		&itype,&dncv,dnp,dzdn, 
		&srtPIAKu,&reliabFlagKu,rrate1d_sub,dn_sub,
		dm_sub,zkuc_sub,piahb_sub,piaKa_sub,zetaS,&piaKuS,&piaKaS);
  //printf("%i \n",bzd);
 
  //if(bzd>100 && bzd<176)
  convretf90_(pRate,dm,dm_sub,rrate1d_sub,&bzd,&bcf,piaKa_sub,piahb_sub,
  	      &srtPIAKu,&piadSRT,&reliabFlagKu,&reliabFlag,zetaS);
  if(isnan(pRate[bcf]))
    {

      for(i=0;i<31;i++)
	printf("%g ",rrate1d_sub[bcf+i*176]);
      printf("\n %g %g\n",piaKuS,piaKaS);
      for(i=0;i<31;i++)
	printf("%g ",zetaS[i]);
      printf("\n");
    }
}
