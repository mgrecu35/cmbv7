#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void pymain_(void);
void mainfortpy_(void);

void open_dpr(char *dprfname);
int read_dpr(int iscan);
void open_dprx(char *dprfname);
int read_dprx(int iscan);
void openoutputfile_(char *jobname, char *fname);
void writescan_(void);
void process_scan(void);
void initp2_(void);
void closeoutputfile_(void);

#include "TKheaders.h"
#include "TK_2ADPR_hdf5.h"
#include "TK_2ADPRX_hdf5.h"
TKINFO dprout_tkfile;



void open_dpr_outputfile_(char *jobname, char *fname)
{
   int status;
   int ret;
   ret = TKopen(fname, "2ADPR", TKWRITE, "HDF5", 
		jobname, &dprout_tkfile,1); 
}

void open_dpr_outputfilex_(char *jobname, char *fname)
{
   int status;
   int ret;
   ret = TKopen(fname, "2ADPRX", TKWRITE, "HDF5", 
		jobname, &dprout_tkfile,1); 
}
void close_dpr_outputfile_()
{
   int status;
   int ret;
   ret = TKclose(&dprout_tkfile);
}
int iLast=0;
int check_scan()
{
  extern L2ADPR_SWATHS dprswath;
  int j, ic=0, ret;
  for(j=0;j<49;j++)
    if(dprswath.NS.VER.heightZeroDeg[j]>500 && dprswath.NS.PRE.flagPrecip[j]>0 &&
       dprswath.NS.SLV.precipRateNearSurface[j]>0.01)
      ic++;
  if((ic>8 || iLast>3) && (dprswath.NS.Latitude[24]-10)*
     (dprswath.NS.Latitude[24]-45)<0)
    {
      ret= TKwriteScan(&dprout_tkfile,&dprswath);
      iLast=ic;
      return 1;
    }
  else
    {
      iLast=ic;
      return 0;
    }
}

int check_scanx()
{
  extern L2ADPRX_SWATHS dprswathx;
  int j, ic=0, ret;
  for(j=0;j<49;j++)
    if(dprswathx.FS.VER.heightZeroDeg[j]>500 && dprswathx.FS.PRE.flagPrecip[j]>0 &&
       dprswathx.FS.SLV.precipRateNearSurface[j]>0.01)
      ic++;
  if((ic>8 || iLast>3) && (dprswathx.FS.Latitude[24]-10)*
     (dprswathx.FS.Latitude[24]-45)<0)
    {
      ret= TKwriteScan(&dprout_tkfile,&dprswathx);
      iLast=ic;
      return 1;
    }
  else
    {
      iLast=ic;
      return 0;
    }
}

int main(int argc, char *argv[])
{
  char *fname;
  fname=(char*)malloc(sizeof(char)*250);
  strcpy(fname,argv[1]);
  mainfortpy_();
  initp2_();
  printf("%s \n",fname);
  open_dpr(fname);
  int istat=0, nscans=0, ioro=0;
  //open_dpr_outputfile_("junk2", argv[2]);
  openoutputfile_("junk2", argv[2]);
  while(istat>=0 && nscans<8000)
    {
      istat=read_dpr(nscans);
      nscans+=1;
      if((nscans-1)%100==0)
      printf("%i \n",nscans);
      //ioro+=check_scanx();
      if(istat>=0)
	{
	  process_scan();
	  writescan_();
	}
    }

  printf("%s %4i %4i\n",fname,nscans,ioro);
  extern TKINFO dprtkfile;
  int ret = TKclose(&dprtkfile);
  closeoutputfile_();
  //  ret = TKclose(&dprout_tkfile);
  //close_dpr_outputfile_();
  //pymain_();
}
