#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void pymain_(void);
void mainfortpy_(void);

void open_dpr(char *dprfname);
int read_dpr(int iscan);
void openoutputfile_(char *jobname, char *fname);
void writescan_(void);
void process_scan(void);
void initp2_(void);
void closeoutputfile_(void);
int main(int argc, char *argv[])
{
  char *fname;
  fname=(char*)malloc(sizeof(char)*150);
  strcpy(fname,argv[1]);
  mainfortpy_();
  initp2_();
  printf("%s \n",fname);
  open_dpr(fname);
  int istat=0, nscans=0;
  openoutputfile_("junk", argv[2]);
  while(istat>=0 && nscans<8000)
    {
      istat=read_dpr(nscans);
      nscans+=1;
      if((nscans-1)%100==0)
	printf("%i \n",nscans);
      if(istat>=0)
	{
	  process_scan();
	  writescan_();
	}
    }

  printf("%s %4i\n",fname,nscans);
  closeoutputfile_();
  //pymain_();
}
