#pragma rtGlobals=1		// Use modern global access method.
Function usfn()
    variable r1,r2,dr,freq=30
    Prompt freq, "Enter frequency (MHz): "
    DoPrompt "Enter frequency", freq
    r1=xcsr(A); r2=xcsr(B)
    dr=r2-r1-50
    WaveStats re
    duplicate re reoffset,reoffset2
    reoffset2=reoffset-V_avg
    duplicate reoffset2 reoffset2disp
    duplicate reoffset2 resa,ress,ressdisp;duplicate retime restimea,restimes,resstimedisp;DeletePoints 0,r1-(1/(freq*1e+6))/1e-10,resa,restimea;DeletePoints ((1/(freq*1e+6))/1e-10)*4.25,250000, resa,restimea
    DeletePoints 0,r1-((1/(freq*1e+6))/1e-10), ress,restimes;DeletePoints r2-((1/(freq*1e+6))/1e-10)+((1/(freq*1e+6))/1e-10)*4.25-r1+((1/(freq*1e+6))/1e-10),250000, ress,restimes
    DeletePoints 0,r2-((1/(freq*1e+6))/1e-10), ressdisp,resstimedisp;DeletePoints  ((1/(freq*1e+6))/1e-10)*4.25,250000, ressdisp,resstimedisp
    display reoffset2disp vs retime;appendtograph reoffset2 vs retime;appendtograph ressdisp vs resstimedisp;appendtograph resa vs restimea;ModifyGraph rgb(resa)=(0,0,65535),rgb(ressdisp)=(0,0,0);ModifyGraph rgb(reoffset2disp)=(52428,52425,1)
    duplicate ress ress0,overlap;ress0=ress*-1;overlap=ress*-1;DeletePoints 0,dr-1, ress0
    Make/N=101/D ressf
    variable t
    for(t=0;t<101;t+=1)
        DeletePoints 0,1,ress0
        duplicate/O ress0 ressd
        ressd=resa*ress0
        Integrate ressd/D=ressd_INT
        duplicate resa resa2; resa2=resa*resa;Integrate resa2/D=resa2_INT
        duplicate ress0 ress02; ress02=ress0*ress0;Integrate ress02/D=ress02_INT
        duplicate ressd_INT ressd_INT2
        ressd_INT2=ressd_INT/((resa2_INT^(1/2))*(ress02_INT^(1/2)))
        ressf[t]=ressd_INT2[((1/(freq*1e+6))/1e-10)*4.25-27]
        Killwaves ressd_INT,resa2_INT,ress02_INT,ressd_INT2,resa2,ress02
    endfor
    make/N=101/D ressftime
    variable i
    for(i=0;i<101;i+=1)
        ressftime[i]=(r2-r1-50+i)*1e-10
    endfor
    make/N=200/D fitressftime
    variable j
    for(j=0;j<200;j+=1)
        fitressftime[j]=(r2-r1-50+j*0.25126*2)*1e-10
    endfor
    CurveFit sin  ressf /D ;display ressf vs ressftime;appendtograph fit_ressf vs fitressftime;ModifyGraph rgb(fit_ressf)=(0,0,65535);ModifyGraph mode(ressf)=3;Label bottom "Two-way travel time (s)"
    variable dP,dT
    dP=(1.570796327-K3)/K2
    dT=(dr+dP)*1e-10
    Print dP
    Print "Two-way travel time: ", dT
    Deletepoints 0,dr+dP,overlap
    Duplicate restimes restimeso,restimeso2
    Deletepoints 0,dr+dP,restimeso
    restimeso2=restimeso-dT
    display resa vs restimea;appendtograph overlap vs restimeso2;ModifyGraph rgb(resa)=(0,0,65535);ModifyGraph rgb(overlap)=(0,0,0)
End