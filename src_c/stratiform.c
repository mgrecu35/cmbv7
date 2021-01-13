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

void stratiform(int btop,int bzd,int bcf,int bsfc, int binBB, int binBBT, float *zKu, float *zKa,
		float srtPIAKu, int reliabFlagKu, float piadSRT, int reliabFlag,
		int *nodes5, float *pRate,
		float *dn, float *dm, float *piaKu, float *piaKa)
{
  float dnCoeff[2]={-0.01257341, -0.00933038};
  int bbb,imu=3,n1d=176,itype=1;
  float piaKuS,piaKaS,dr=0.125,eps=1.0,epst=1.0,dnst=0.0;
  float dpn[176], dzdn[176*176], dpiadn[2*176], dnp[176], zKuC[176], zKaSim[176];
  float dt1,dt2;
  if(binBB>0)
    {
      bbb=binBB+2;
      iter_profst_(&btop,&bzd,&binBB,&binBBT,&bbb,&bcf,&bsfc,
		  zKu,zKa,&dr,&n1d,&eps,&imu,dn,dm,pRate,zKuC,zKaSim,
		  &epst,&piaKu,&piaKa,&dnst,dnCoeff,
		  dnp,dzdn,dpiadn,&piaKuS,&piaKaS);
    }
  else
     iter_profst_nobb_(&btop,&bzd,&bcf,&bsfc,
		       zKu,zKa,&dr,&n1d,&eps,&imu,dn,dm,pRate,zKuC,zKaSim,
		       &epst,&piaKu,&piaKa,&itype,&dnst,dnCoeff,
		       dnp,dzdn,&dt1,&dt2,dpiadn,&piaKuS,&piaKaS);
    
}
