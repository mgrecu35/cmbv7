#include <stdlib.h>
#include <stdio.h>
void stratiform(int btop,int bzd,int bcf,int bsfc, int binBB, int binBBT, float *zKu, float *zKa,
		float srtPIAKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa);
  
void iter_profst_(int *btop,int *bzd,int *bb,int *bbt,int *bbb,int *bcf,int *bsfc,
		 float *zKuL,float *zKaL,float *dr,int *n1d,float *eps,int *imu,
		 float *dn1d,float *dm1d,float *rrate1d,float *zKuC,float *zKaSim,
		 float *epst,float *piaKu,float *piaKa,float *dnst,float *dnCoeff_new,
		 float *dnp,float *dzdn,float *dpiadn,float *piaKuS,float *piaKaS);

void iter_profst_nobb_(int *btop,int *bzd,int *bcf,int *bsfc,float *zKuL,float *zKaL,
		      float *dr,int *n1d,float *eps,int *imu, float *dn1d,
		      float *dm1d,float *rrate1d,float *zKuC,float *zKaSim,float *epst,
		      float *piaKu,float *piaKa,int *itype,float *dnCoeff_new,float *dncv,
		      float *dnp,float *dzdn,float *dt1, float *dt2, float *dpiadn,
		      float *piaKuS, float *piaKaS);


void rainprofstg_(int *n1,float *zku_obs,float *zka_obs,float *dpiaSRT,
		  float *piakus,float *piakas, int *reldpia,
		  int *nc,float *dr,float *wzku,float *wzka,float *wpia,
		  float *rrate_in,float *dn_in,int *nens,
		  float *rrate_out,float *dn_out,float *zkusim,
		  float *zkasim,float *zku_out,float *zka_out,
		  float *rrens,float *yEns,float *xEns,float *dy,
		  float *pia_out,float *dm_out);
  

void stratiform(int btop,int bzd,int bcf,int bsfc, int binBB, int binBBT, float *zKu, float *zKa,
		float srtPIAKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa)
{
  float dnCoeff[2]={-0.01257341, -0.00933038};
  int bbb,imu=3,n1d=176,itype=1;
  float piaKuS,piaKaS,dr=0.125,eps=1.0,epst=1.0,dnst=-0.2;
  float dpn[176], dzdn[176*176], dpiadn[2*176], dnp[176], zKuC[176], zKaSim[176];
  float dt1,dt2;
  int i;
  for(i=0;i<176;i++)
    dnp[i]=0;
  if(binBB>0)
    {
      bbb=binBB+2;
      iter_profst_(&btop,&bzd,&binBB,&binBBT,&bbb,&bcf,&bsfc,
		  zKu,zKa,&dr,&n1d,&eps,&imu,dn,dm,pRate,zKuC,zKaSim,
		  &epst,piaKu,piaKa,&dnst,dnCoeff,
		  dnp,dzdn,dpiadn,&piaKuS,&piaKaS);
    }
  else
    {
      /*iter_profst_nobb(btop,bzd,bcf,bsfc,zKuL,zKaL,dr,n1d,eps,imu,&
     dn1d,dm1d,rrate1d,zKuC,zKaSim,epst,piaKu,piaKa,itype,dnCoeff_new,&
     dncv,dnp,dzdn,&
     dt1,dt2, dpiadn, piaKuS, piaKaS)
      */
      iter_profst_nobb_(&btop,&bzd,&bcf,&bsfc,
			zKu,zKa,&dr,&n1d,&eps,&imu,dn,dm,pRate,zKuC,zKaSim,
			&epst,piaKu,piaKa,&itype,dnCoeff,
			&dnst,dnp,dzdn,&dt1,&dt2,dpiadn,&piaKuS,&piaKaS);
      bbb=bzd+2;
    }
  int n1=bcf-bbb+1;
  float wzku=0.2,wzka=0.1,wpia=1;
  int nens=60, nc;
  float *pRate_out,*dn_out,*zkusimE,*zkasimE,
    *zku_out,*zka_out,*rrEns,*yEns,*xEns,*dy,*pia_out,*dmOut,*attOut,*zkusim,*zkasim;
  nc=bsfc-bcf;
  if(n1>1)
    {
      //printf("%i %i %i %g %g \n",n1, bbb,bcf,piaKaS,piaKuS);
      pRate_out=(float*)malloc(sizeof(float)*n1);
      dn_out=(float*)malloc(sizeof(float)*n1);
      zku_out=(float*)malloc(sizeof(float)*n1);
      zka_out=(float*)malloc(sizeof(float)*n1);
      dmOut=(float*)malloc(sizeof(float)*n1);
      attOut=(float*)malloc(sizeof(float)*n1*2);
      pia_out=(float*)malloc(sizeof(float)*2);
      rrEns=(float*)malloc(sizeof(float)*n1*nens);
      yEns=(float*)malloc(sizeof(float)*nens*(2*n1+1));
      xEns=(float*)malloc(sizeof(float)*nens*(2*n1+1));
      dy=(float*)malloc(sizeof(float)*(2*n1+1));
      zkusim=(float*)malloc(sizeof(float)*(nens*n1));
      zkasim=(float*)malloc(sizeof(float)*(nens*n1));
      //rrens(nens,n1),pia_out(2),yEns(nens,2*n1+1),xEns(nens,2*n1+1), dy(2*n1+1)
      rainprofstg_(&n1,&zKu[bbb],&zKa[bbb],&piadSRT,&piaKuS,&piaKaS,&reliabFlag,
		   &nc,&dr,&wzku,&wzka,&wpia,&pRate[bbb],&dn[bbb],&nens,
		   pRate_out,dn_out,zkusim,zkasim,zku_out,zka_out,
		   rrEns,yEns,xEns,dy,pia_out,dmOut);
      int k;
      if(pRate_out[n1-1]<0)
	{
	  for(k=0;k<n1;k++)
	    printf("%g ",pRate_out[k]);
	  printf("\n");
	  exit(0);
	}
      for(k=0;k<n1;k++)
	pRate[bbb+k]=pRate_out[k];
      
      /* rainprofstg_(int *n1,float *zku_obs,float *zka_obs,float *dpiaSRT,
	 float *piakus,float *piakas, int *reldpia,
	 int *nc,float *dr,float *wzku,float *wzka,float *wpia,
	 float *rrate_in,float *dn_in,int *nens,
	 float *rrate_out,float *dn_out,float *zkusim,
	 float *zkasim,float *zku_out,float *zka_out,
	 float *rrens,float *yEns,float *xEns,float *dy,
	 float *pia_out,float *dm_out);*/
      free(pRate_out);
      free(dn_out);
      free(zku_out);
      free(zka_out);
      free(dmOut);
      free(attOut);
      free(pia_out);
      free(rrEns);
      free(yEns);
      free(xEns);
      free(dy);
      free(zkusim);
      free(zkasim);
    }
}
