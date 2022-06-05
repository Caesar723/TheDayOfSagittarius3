#include <iostream>
#include <cmath>


using namespace std;

bool checkInRange(int (*filghts)[4],int y,int x,int MyLen,int radius){  // check opponent ship whether in the visible area
    int index;
    for(index=0;index<MyLen;index++){
        
        if (pow(y-filghts[index][0],2)+pow(x-filghts[index][1],2)<=pow(radius,2)){
            
            return true ;
        }
    }
    return false;
}////

void drawLines(int (*map)[5000*3],double k,double b,int *rgb,double *pos1,double *pos2,int *filghts){
    int y,x,index,element;
    
    if (abs(k)>1){
        for(index=(int)std::min(pos1[0],pos2[0]);index<(int)std::max(pos1[0],pos2[0]);index++){
            x=(int)((index-b)/k);
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && x+filghts[1] >=0 && x+filghts[1]<=5000){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][((x+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        } 
    }
    else{
        for(index=(int)std::min(pos1[1],pos2[1]);index<(int)std::max(pos1[1],pos2[1]);index++){
            y=k*index+b;
            if (filghts[0]+y>=0 && filghts[0]+y<10000 && index+filghts[1] >=0 && index+filghts[1]<=5000){
                for(element=0;element<3;element++){
                    map[y+filghts[0]][((index+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        } 
    }
}

void drawOppoLines(int (*map)[5000*3],double k,double b,int *rgb,double *pos1,double *pos2,int *filghts,int (*CheckFlights)[4],int Flen){
    int y,x,index,element;
    
    if (abs(k)>1){
        for(index=(int)std::min(pos1[0],pos2[0]);index<(int)std::max(pos1[0],pos2[0]);index++){
            x=(int)((index-b)/k);
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && x+filghts[1] >=0 && x+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],x+filghts[1],Flen,200)){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][((x+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        } 
    }
    else{
        for(index=(int)std::min(pos1[1],pos2[1]);index<(int)std::max(pos1[1],pos2[1]);index++){
            y=k*index+b;
            if (filghts[0]+y>=0 && filghts[0]+y<10000 && index+filghts[1] >=0 && index+filghts[1]<=5000 && checkInRange(CheckFlights,y+filghts[0],index+filghts[1],Flen,200)){
                for(element=0;element<3;element++){
                    map[y+filghts[0]][((index+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        } 
    }
}

void simpleSort(double (*imfo)[5]){
    double fir;
    for (int ii=2;ii>0;ii--){
        for (int i=0;i<ii;i++){
            if (imfo[i][0]>imfo[i+1][0]){
                for(int collect=0;collect<5;collect++){
                    fir=imfo[i][collect];
                    imfo[i][collect]=imfo[i+1][collect];
                    imfo[i+1][collect]=fir;
                }
                
            }
        }
    }
}
void sortR(double (*imfo)[6],int length){
    double lowest,regis;
    int index,index2,recordIndex;
    double record;
    for (index=0;index<length;index++){
        lowest=imfo[index][0];
        recordIndex=index;
        for (index2=index;index2<length;index2++){
            if (imfo[index2][0]<lowest){
                recordIndex=index2;
                lowest=imfo[index2][0];
            }
        }
        for(index2=0;index2<5;index2++){
            record=imfo[recordIndex][index2];
            imfo[recordIndex][index2]=imfo[index][index2];
            imfo[index][index2]=record;
        }
    }
}

void drawArea(double (*imfo)[5],int (*map)[5000*3],int *filghts,int *rgb){//128 165 242
    double y1,y2,i;
    int index,element;
    //int rgb[]={128,165,242};
    
    for(i=imfo[0][0];i<imfo[1][0];i++){
        y1=i*imfo[0][1]+imfo[0][2];
        y2=i*imfo[0][3]+imfo[0][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        }
    }
    for(i=imfo[1][0];i<imfo[2][0];i++){
        y1=i*imfo[2][1]+imfo[2][2];
        y2=i*imfo[2][3]+imfo[2][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }
}

void drawOppoArea(double (*imfo)[5],int (*map)[5000*3],int *filghts,int *rgb,int (*CheckFlights)[4],int Flen){//it is similar as drawArea but it can check the visible area 
    double y1,y2,i;
    int index,element;
    
    for(i=imfo[0][0];i<imfo[1][0];i++){
        y1=i*imfo[0][1]+imfo[0][2];
        y2=i*imfo[0][3]+imfo[0][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],(int)i+filghts[1],Flen,200)){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        }
    }
    for(i=imfo[1][0];i<imfo[2][0];i++){
        y1=i*imfo[2][1]+imfo[2][2];
        y2=i*imfo[2][3]+imfo[2][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],(int)i+filghts[1],Flen,200)){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }
}

void drawMyFlight(int (*map)[5000*3],int (*filghts),int *rgb,int *rgbBody){// y,x,size,angle 49,74,231
    
    int element,index,Line;
    double Rad=filghts[3]*3.14159/180;
    double head[2],tail[2],sideL[2],sideR[2];//[y,x]
    
    head[0]=-sin(Rad)*filghts[2],head[1]=cos(Rad)*filghts[2];
    tail[0]=sin(Rad)*(filghts[2]/2),tail[1]=-cos(Rad)*(filghts[2]/2);
    double k=(head[0])/(head[1]);
    double pdk=-1/k;
    double b=tail[0]-pdk*tail[1];

    sideL[1]=sqrt(pow(filghts[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideL[0]=(sideL[1]-tail[1])*pdk+tail[0];
    sideR[1]=-sqrt(pow(filghts[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideR[0]=-(sideL[1]-tail[1])*pdk+tail[0];
    double leftK=(head[0]-sideL[0])/(head[1]-sideL[1]),rightK=(head[0]-sideR[0])/(head[1]-sideR[1]);


    double leftLeft[2],headLeft[2],rightLeft[2],leftRight[2],headRight[2],rightRight[2];
    leftLeft[1]=sqrt(pow(filghts[2]/4,2)/(pow(pdk,2)+1))+sideL[1],leftLeft[0]=(leftLeft[1]-sideL[1])*pdk+sideL[0];
    rightLeft[1]=-sqrt(pow(filghts[2]/4,2)/(pow(pdk,2)+1))+sideR[1],rightLeft[0]=(rightLeft[1]-sideR[1])*pdk+sideR[0];
    
    leftRight[1]=(leftK>0 && (filghts[3]>270 ||filghts[3]<90) ?1:-1)*(filghts[3]<90 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(leftK,2)+1))+sideL[1],leftRight[0]=(leftRight[1]-sideL[1])*leftK+sideL[0];
    headLeft[1]=(leftK>0 && (filghts[3]>270 ||filghts[3]<90) ?-1:1)*(filghts[3]<90 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(leftK,2)+1))+head[1],headLeft[0]=(headLeft[1]-head[1])*leftK+head[0];
    
    rightRight[1]=(rightK>0 && (filghts[3]>=90 &&filghts[3]<270) ?1:-1)*(filghts[3]<=180 || filghts[3]>=270 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(rightK,2)+1))+sideR[1],rightRight[0]=(rightRight[1]-sideR[1])*rightK+sideR[0];
    headRight[1]=(rightK>0 && (filghts[3]>=90 &&filghts[3]<270) ?-1:1)*(filghts[3]<=180 || filghts[3]>=270 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(rightK,2)+1))+head[1],headRight[0]=(headRight[1]-head[1])*rightK+head[0];
    
    double bL=sideL[0]-leftK*sideL[1],bR=sideR[0]-rightK*sideR[1];
    
    
    
    double smallKL,smallBL;
    smallKL=(leftLeft[0]-leftRight[0])/(leftLeft[1]-leftRight[1]);
    smallBL=leftLeft[0]-leftLeft[1]*smallKL;
    
    double smallKH=(headLeft[0]-headRight[0])/(headLeft[1]-headRight[1]),smallBH=headRight[0]-headRight[1]*smallKH;
    

    double smallKR=(rightLeft[0]-rightRight[0])/(rightLeft[1]-rightRight[1]),smallBR=rightLeft[0]-rightLeft[1]*smallKR;
    
    
    
    double arrayH[3][5]={//x k b k b
        {head[1],leftK,bL,rightK,bR},
        {headLeft[1],leftK,bL,smallKH,smallBH},
        {headRight[1],rightK,bR,smallKH,smallBH}
    };
    simpleSort(arrayH);
    drawArea(arrayH,map,filghts,rgbBody);

    double arrayL[3][5]={
        {leftLeft[1],pdk,b,smallKL,smallBL},
        {leftRight[1],leftK,bL,smallKL,smallBL},
        {sideL[1],pdk,b,leftK,bL}
    };
    simpleSort(arrayL);
    drawArea(arrayL,map,filghts,rgbBody);

    double arrayR[3][5]={
        {rightLeft[1],pdk,b,smallKR,smallBR},
        {rightRight[1],rightK,bR,smallKR,smallBR},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayR);
    drawArea(arrayR,map,filghts,rgbBody);

    double arrayB[3][5]={
        {head[1],leftK,bL,rightK,bR},
        {sideL[1],pdk,b,leftK,bL},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayB);
    drawArea(arrayB,map,filghts,rgbBody);

    drawLines(map,pdk,b,rgb,leftLeft,rightLeft,filghts);
    drawLines(map,leftK,bL,rgb,leftRight,headLeft,filghts);
    drawLines(map,rightK,bR,rgb,rightRight,headRight,filghts);
    drawLines(map,smallKL,smallBL,rgb,leftLeft,leftRight,filghts);
    drawLines(map,smallKH,smallBH,rgb,headLeft,headRight,filghts);
    drawLines(map,smallKR,smallBR,rgb,rightLeft,rightRight,filghts);
    
}

void drawOppoFlight(int (*map)[5000*3],int (*filghts),int *rgb,int *rgbBody,int (*CheckFlights)[4],int Flen){// it is similar as drawmyFlight but it can check the visible area
    
    int element,index,Line;
    double Rad=filghts[3]*3.14159/180;
    double head[2],tail[2],sideL[2],sideR[2];//[y,x]
    
    head[0]=-sin(Rad)*filghts[2],head[1]=cos(Rad)*filghts[2];
    tail[0]=sin(Rad)*(filghts[2]/2),tail[1]=-cos(Rad)*(filghts[2]/2);
    double k=(head[0])/(head[1]);
    double pdk=-1/k;
    double b=tail[0]-pdk*tail[1];

    sideL[1]=sqrt(pow(filghts[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideL[0]=(sideL[1]-tail[1])*pdk+tail[0];
    sideR[1]=-sqrt(pow(filghts[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideR[0]=-(sideL[1]-tail[1])*pdk+tail[0];
    double leftK=(head[0]-sideL[0])/(head[1]-sideL[1]),rightK=(head[0]-sideR[0])/(head[1]-sideR[1]);


    double leftLeft[2],headLeft[2],rightLeft[2],leftRight[2],headRight[2],rightRight[2];
    leftLeft[1]=sqrt(pow(filghts[2]/4,2)/(pow(pdk,2)+1))+sideL[1],leftLeft[0]=(leftLeft[1]-sideL[1])*pdk+sideL[0];
    rightLeft[1]=-sqrt(pow(filghts[2]/4,2)/(pow(pdk,2)+1))+sideR[1],rightLeft[0]=(rightLeft[1]-sideR[1])*pdk+sideR[0];
    
    leftRight[1]=(leftK>0 && (filghts[3]>270 ||filghts[3]<90) ?1:-1)*(filghts[3]<90 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(leftK,2)+1))+sideL[1],leftRight[0]=(leftRight[1]-sideL[1])*leftK+sideL[0];
    headLeft[1]=(leftK>0 && (filghts[3]>270 ||filghts[3]<90) ?-1:1)*(filghts[3]<90 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(leftK,2)+1))+head[1],headLeft[0]=(headLeft[1]-head[1])*leftK+head[0];
    
    rightRight[1]=(rightK>0 && (filghts[3]>=90 &&filghts[3]<270) ?1:-1)*(filghts[3]<=180 || filghts[3]>=270 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(rightK,2)+1))+sideR[1],rightRight[0]=(rightRight[1]-sideR[1])*rightK+sideR[0];
    headRight[1]=(rightK>0 && (filghts[3]>=90 &&filghts[3]<270) ?-1:1)*(filghts[3]<=180 || filghts[3]>=270 ? 1:-1)*sqrt(pow(filghts[2]/4,2)/(pow(rightK,2)+1))+head[1],headRight[0]=(headRight[1]-head[1])*rightK+head[0];
    
    double bL=sideL[0]-leftK*sideL[1],bR=sideR[0]-rightK*sideR[1];
    
    
    
    double smallKL,smallBL;
    smallKL=(leftLeft[0]-leftRight[0])/(leftLeft[1]-leftRight[1]);
    smallBL=leftLeft[0]-leftLeft[1]*smallKL;
    
    double smallKH=(headLeft[0]-headRight[0])/(headLeft[1]-headRight[1]),smallBH=headRight[0]-headRight[1]*smallKH;
    

    double smallKR=(rightLeft[0]-rightRight[0])/(rightLeft[1]-rightRight[1]),smallBR=rightLeft[0]-rightLeft[1]*smallKR;
    
    
    
    double arrayH[3][5]={//x k b k b
        {head[1],leftK,bL,rightK,bR},
        {headLeft[1],leftK,bL,smallKH,smallBH},
        {headRight[1],rightK,bR,smallKH,smallBH}
    };
    simpleSort(arrayH);
    drawOppoArea(arrayH,map,filghts,rgbBody,CheckFlights,Flen);

    double arrayL[3][5]={
        {leftLeft[1],pdk,b,smallKL,smallBL},
        {leftRight[1],leftK,bL,smallKL,smallBL},
        {sideL[1],pdk,b,leftK,bL}
    };
    simpleSort(arrayL);
    drawOppoArea(arrayL,map,filghts,rgbBody,CheckFlights,Flen);

    double arrayR[3][5]={
        {rightLeft[1],pdk,b,smallKR,smallBR},
        {rightRight[1],rightK,bR,smallKR,smallBR},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayR);
    drawOppoArea(arrayR,map,filghts,rgbBody,CheckFlights,Flen);

    double arrayB[3][5]={
        {head[1],leftK,bL,rightK,bR},
        {sideL[1],pdk,b,leftK,bL},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayB);
    drawOppoArea(arrayB,map,filghts,rgbBody,CheckFlights,Flen);

    drawOppoLines(map,pdk,b,rgb,leftLeft,rightLeft,filghts,CheckFlights,Flen);
    drawOppoLines(map,leftK,bL,rgb,leftRight,headLeft,filghts,CheckFlights,Flen);
    drawOppoLines(map,rightK,bR,rgb,rightRight,headRight,filghts,CheckFlights,Flen);
    drawOppoLines(map,smallKL,smallBL,rgb,leftLeft,leftRight,filghts,CheckFlights,Flen);
    drawOppoLines(map,smallKH,smallBH,rgb,headLeft,headRight,filghts,CheckFlights,Flen);
    drawOppoLines(map,smallKR,smallBR,rgb,rightLeft,rightRight,filghts,CheckFlights,Flen);
    
}

void drawAVisible(int (*map)[5000*3],int (*filghts),int radius){
    int element,vertical,points,ponXL,ponXR,ponY,rgb;
    int rgbL[]={42,45,84},rgbB[]={102,156,177};
    for(points=0;points<radius;points++){
        ponXL=filghts[1]-points;
        ponY= (int) sqrt(pow(radius,2)-pow(points,2))+0.5;
        for (vertical=-ponY;vertical<ponY;vertical++){
            if (filghts[0]+vertical>=0 && filghts[0]+vertical<10000 && ponXL>=0 && ponXL<5000){
                if (map[filghts[0]+vertical][ponXL*3]==34 ){
                    for (element=0;element<3;element++ ){
                    
                        map[filghts[0]+vertical][ponXL*3+element]=rgbB[element];
                                
                        
                    }
                }
                else if(map[filghts[0]+vertical][ponXL*3]==14){
                    for (element=0;element<3;element++ ){
                    
                        map[filghts[0]+vertical][ponXL*3+element]=rgbL[element];
                                
                        
                    }
                }
                
            }
            
            if (filghts[0]+vertical>=0 && filghts[0]+vertical<10000 && filghts[1]+points>=0 && filghts[1]+points<5000){
                if (map[filghts[0]+vertical][(filghts[1]+points)*3]==34 ){
                    for (element=0;element<3;element++ ){
                        
                        map[filghts[0]+vertical][(filghts[1]+points)*3+element]=rgbB[element];
                                
                        
                    }
                }
                else if(map[filghts[0]+vertical][(filghts[1]+points)*3]==14){
                    for (element=0;element<3;element++ ){
                        map[filghts[0]+vertical][(filghts[1]+points)*3+element]=rgbL[element];
                    }
                }
            }
        }
        
    }
}

void drawAScout(int (*map)[5000*3],int (*scout),int *rgbBody,int radius){
    int element,vertical,points,ponXL,ponXR,ponY,rgb;
    for(points=0;points<radius;points++){
        ponXL=scout[1]-points;
        ponY= (int) sqrt(pow(radius,2)-pow(points,2))+0.5;
        for (vertical=-ponY;vertical<ponY;vertical++){
            if (scout[0]+vertical>=0 && scout[0]+vertical<10000 && ponXL>=0 && ponXL<5000){
                
                for (element=0;element<3;element++ ){
                
                    map[scout[0]+vertical][ponXL*3+element]=rgbBody[element];
                            
                    
                }
                
            }
            
            if (scout[0]+vertical>=0 && scout[0]+vertical<10000 && scout[1]+points>=0 && scout[1]+points<5000){
                
                for (element=0;element<3;element++ ){
                    
                    map[scout[0]+vertical][(scout[1]+points)*3+element]=rgbBody[element];
                            
                    
                }
                
            }
        }
        
    }
}

void drawAOppoScout(int (*map)[5000*3],int (*scout),int *rgbBody,int radius,int (*CheckFlights)[4],int Flen){
    int element,vertical,points,ponXL,ponXR,ponY,rgb;
    for(points=0;points<radius;points++){
        ponXL=scout[1]-points;
        ponY= (int) sqrt(pow(radius,2)-pow(points,2))+0.5;
        for (vertical=-ponY;vertical<ponY;vertical++){
            if (scout[0]+vertical>=0 && scout[0]+vertical<10000 && ponXL>=0 && ponXL<5000 && checkInRange(CheckFlights,scout[0]+vertical,ponXL,Flen,200)){
                
                for (element=0;element<3;element++ ){
                
                    map[scout[0]+vertical][ponXL*3+element]=rgbBody[element];
                            
                    
                }
                
            }
            
            if (scout[0]+vertical>=0 && scout[0]+vertical<10000 && scout[1]+points>=0 && scout[1]+points<5000 && checkInRange(CheckFlights,scout[0]+vertical,scout[1]+points,Flen,200)){
                
                for (element=0;element<3;element++ ){
                    
                    map[scout[0]+vertical][(scout[1]+points)*3+element]=rgbBody[element];
                            
                    
                }
                
            }
        }
        
    }
}


void drawOneTriangle(int (*map)[5000*3],double (*tail),double (*head),int (*start),int (*rgbBody),double pdk,int radius){
    double sideL[2],sideR[2];
    double b=tail[0]-pdk*tail[1];
    
    sideL[1]=sqrt(pow(radius,2)/(pow(pdk,2)+1))+tail[1],sideL[0]=(sideL[1]-tail[1])*pdk+tail[0];
    sideR[1]=-sqrt(pow(radius,2)/(pow(pdk,2)+1))+tail[1],sideR[0]=-(sideL[1]-tail[1])*pdk+tail[0];
    double leftK=(head[0]-sideL[0])/(head[1]-sideL[1]),rightK=(head[0]-sideR[0])/(head[1]-sideR[1]);
    double bL=sideL[0]-leftK*sideL[1],bR=sideR[0]-rightK*sideR[1];
    double arrayB[3][5]={
        {head[1],leftK,bL,rightK,bR},
        {sideL[1],pdk,b,leftK,bL},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayB);
    drawArea(arrayB,map,start,rgbBody);
}

void drawOneOppoTriangle(int (*map)[5000*3],double (*tail),double (*head),int (*start),int (*rgbBody),double pdk,int radius,int (*CheckFlights)[4],int Flen){
    double sideL[2],sideR[2];
    double b=tail[0]-pdk*tail[1];
    
    sideL[1]=sqrt(pow(radius,2)/(pow(pdk,2)+1))+tail[1],sideL[0]=(sideL[1]-tail[1])*pdk+tail[0];
    sideR[1]=-sqrt(pow(radius,2)/(pow(pdk,2)+1))+tail[1],sideR[0]=-(sideL[1]-tail[1])*pdk+tail[0];
    double leftK=(head[0]-sideL[0])/(head[1]-sideL[1]),rightK=(head[0]-sideR[0])/(head[1]-sideR[1]);
    double bL=sideL[0]-leftK*sideL[1],bR=sideR[0]-rightK*sideR[1];
    double arrayB[3][5]={
        {head[1],leftK,bL,rightK,bR},
        {sideL[1],pdk,b,leftK,bL},
        {sideR[1],pdk,b,rightK,bR}
    };
    simpleSort(arrayB);
    drawOppoArea(arrayB,map,start,rgbBody,CheckFlights,Flen);
}

void FillAVisible(int (*map)[5000*3],int (*filghts),int radius){
    int element,vertical,points,ponXL,ponXR,ponY,rgb,thi,thick=4;
    int rgbB[]={14, 15, 28},rgbL[]={34,52,59};
    for(points=0;points<radius;points++){
        ponXL=filghts[1]-points;
        ponY= (int) sqrt(pow(radius,2)-pow(points,2))+0.5;
        for (vertical=-ponY;vertical<ponY;vertical++){
            if (filghts[0]+vertical>=0 && filghts[0]+vertical<10000 && ponXL>=0 && ponXL<5000){

                if ((filghts[0]+vertical)%100==0){
                    for (element=0;element<3;element++ ){
                        for (thi=0;thi<thick;thi++){
                            map[filghts[0]+vertical+thi][ponXL*3+element]=rgbL[element];
                        }
                    }
                }
                else if(ponXL%100==0){
                    for (element=0;element<3;element++ ){
                        for (thi=0;thi<thick;thi++){
                            map[filghts[0]+vertical][(ponXL+thi)*3+element]=rgbL[element];
                        }
                        
                    }
                }
                else if (map[filghts[0]+vertical][ponXL*3]!=34){
                    for (element=0;element<3;element++ ){
                    
                        map[filghts[0]+vertical][ponXL*3+element]=rgbB[element];
                                
                        
                    }
                }
                
            }
            
            if (filghts[0]+vertical>=0 && filghts[0]+vertical<10000 && filghts[1]+points>=0 && filghts[1]+points<5000){
                if ((filghts[0]+vertical)%100==0){
                    for (element=0;element<3;element++ ){
                        for (thi=0;thi<thick;thi++){
                            map[filghts[0]+vertical+thi][(filghts[1]+points)*3+element]=rgbL[element];
                        }
                    }
                }
                else if((filghts[1]+points)%100==0){
                    for (element=0;element<3;element++ ){
                        for (thi=0;thi<thick;thi++){
                            map[filghts[0]+vertical][(filghts[1]+points+thi)*3+element]=rgbL[element];
                        }
                    }
                }
                else if (map[filghts[0]+vertical][(filghts[1]+points)*3]!=34){
                    for (element=0;element<3;element++ ){
                        map[filghts[0]+vertical][(filghts[1]+points)*3+element]=rgbB[element];
                    }
                }
            }
        }
        
    }
}

void fillAreaRec(double (*imfo)[6],int (*map)[5000*3],int *filghts,int *rgb,double k1,double b1,double k2,double b2){
    double y1,y2,i;
    int index,element;
    //int rgb[]={128,165,242};
    
    for(i=imfo[0][0];i<imfo[1][0];i++){
        y1=i*imfo[0][1]+imfo[0][2];
        y2=i*imfo[0][3]+imfo[0][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        }
    }
    for(i=imfo[2][0];i<imfo[3][0];i++){
        y1=i*imfo[3][1]+imfo[3][2];
        y2=i*imfo[3][3]+imfo[3][4];
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }
    for(i=imfo[1][0];i<imfo[2][0];i++){
        y1=i*k1+b1;
        y2=i*k2+b2;
        for (index=(int)std::min(y1,y2);index<(int)std::max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }

}

void fillOppoRec(double (*imfo)[6],int (*map)[5000*3],int *filghts,int *rgb,double k1,double b1,double k2,double b2,int (*CheckFlights)[4],int Flen){
    double y1,y2,i;
    int index,element;
    //int rgb[]={128,165,242};
    
    for(i=imfo[0][0];i<imfo[1][0];i++){
        y1=i*imfo[0][1]+imfo[0][2];
        y2=i*imfo[0][3]+imfo[0][4];
        for (index=(int)min(y1,y2);index<(int)max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],(int)i+filghts[1],Flen,200)){
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
            
        }
    }
    for(i=imfo[2][0];i<imfo[3][0];i++){
        y1=i*imfo[3][1]+imfo[3][2];
        y2=i*imfo[3][3]+imfo[3][4];
        for (index=(int)min(y1,y2);index<(int)max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],(int)i+filghts[1],Flen,200)){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }
    for(i=imfo[1][0];i<imfo[2][0];i++){
        y1=i*k1+b1;
        y2=i*k2+b2;
        for (index=(int)min(y1,y2);index<(int)max(y1,y2);index++){
            if (filghts[0]+index>=0 && filghts[0]+index<10000 && (int)i+filghts[1] >=0 && (int)i+filghts[1]<=5000 && checkInRange(CheckFlights,index+filghts[0],(int)i+filghts[1],Flen,200)){
            
                for(element=0;element<3;element++){
                    map[index+filghts[0]][(((int)i+filghts[1])*3)+element]=rgb[element];
                }
            }
        }
    }
}

void drawRectangle(int (*map)[5000*3],int (*position),int *rgb){
    double Rad=position[3]*3.14159/180;
    double head[2],tail[2],sideTL[2],sideTR[2],sideHL[2],sideHR[2];
    head[0]=-sin(Rad)*position[2],head[1]=cos(Rad)*position[2];
    int Point[]={(int)head[0]+position[0],(int)head[1]+position[1]};
    drawAScout(map,Point,rgb,position[2]/2);
    tail[0]=sin(Rad)*(position[2]),tail[1]=-cos(Rad)*(position[2]);
    double k=(head[0])/(head[1]);
    
    double pdk=-1/k;
    double pdHb=head[0]-pdk*head[1];
    double pdTb=tail[0]-pdk*tail[1];
    sideTL[1]=sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideTL[0]=(sideTL[1]-tail[1])*pdk+tail[0];
    sideTR[1]=-sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideTR[0]=-(sideTL[1]-tail[1])*pdk+tail[0];
    
    sideHL[1]=sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+head[1],sideHL[0]=(sideHL[1]-head[1])*pdk+head[0];
    sideHR[1]=-sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+head[1],sideHR[0]=-(sideHL[1]-head[1])*pdk+head[0];

    double Lb=sideTL[0]-k*sideTL[1];
    double Rb=sideTR[0]-k*sideTR[1];




    double arrayH[4][6]={//x k b k b
        {sideTL[1],pdk,pdTb,k,Lb ,sideTL[0]},
        {sideTR[1],pdk,pdTb,k,Rb,sideTR[0]},
        {sideHL[1],pdk,pdHb,k,Lb,sideHL[0]},
        {sideHR[1],pdk,pdHb,k,Rb,sideHR[0]}
    };
    
    sortR(arrayH,4);
    if (arrayH[1][0]==sideTR[1] && sideTR[1]<sideHL[1]  ||  arrayH[1][0]==sideHR[1] && sideTL[1]>sideHR[1]){
        
        fillAreaRec(arrayH,map,position,rgb,pdk,pdHb,pdk,pdTb);
    }
    else{
        
        fillAreaRec(arrayH,map,position,rgb,k,Lb,k,Rb);
    }
    
}

void drawOppoRectangle(int (*map)[5000*3],int (*position),int *rgb,int (*CheckFlights)[4],int Flen){
    double Rad=position[3]*3.14159/180;
    double head[2],tail[2],sideTL[2],sideTR[2],sideHL[2],sideHR[2];
    head[0]=-sin(Rad)*position[2],head[1]=cos(Rad)*position[2];
    int Point[]={(int)head[0]+position[0],(int)head[1]+position[1]};
    drawAOppoScout(map,Point,rgb,position[2]/2,CheckFlights,Flen);
    tail[0]=sin(Rad)*(position[2]),tail[1]=-cos(Rad)*(position[2]);
    double k=(head[0])/(head[1]);
    
    double pdk=-1/k;
    double pdHb=head[0]-pdk*head[1];
    double pdTb=tail[0]-pdk*tail[1];
    sideTL[1]=sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideTL[0]=(sideTL[1]-tail[1])*pdk+tail[0];
    sideTR[1]=-sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+tail[1],sideTR[0]=-(sideTL[1]-tail[1])*pdk+tail[0];
    
    sideHL[1]=sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+head[1],sideHL[0]=(sideHL[1]-head[1])*pdk+head[0];
    sideHR[1]=-sqrt(pow(position[2]/2,2)/(pow(pdk,2)+1))+head[1],sideHR[0]=-(sideHL[1]-head[1])*pdk+head[0];

    double Lb=sideTL[0]-k*sideTL[1];
    double Rb=sideTR[0]-k*sideTR[1];




    double arrayH[4][6]={//x k b k b
        {sideTL[1],pdk,pdTb,k,Lb ,sideTL[0]},
        {sideTR[1],pdk,pdTb,k,Rb,sideTR[0]},
        {sideHL[1],pdk,pdHb,k,Lb,sideHL[0]},
        {sideHR[1],pdk,pdHb,k,Rb,sideHR[0]}
    };
    
    sortR(arrayH,4);
    if (arrayH[1][0]==sideTR[1] && sideTR[1]<sideHL[1]  ||  arrayH[1][0]==sideHR[1] && sideTL[1]>sideHR[1]){
        
        fillOppoRec(arrayH,map,position,rgb,pdk,pdHb,pdk,pdTb,CheckFlights,Flen);
    }
    else{
        
        fillOppoRec(arrayH,map,position,rgb,k,Lb,k,Rb,CheckFlights,Flen);
    }
}

void drawOppoLaser(int (*map)[5000*3],int (*start),int(*end),int timeParam,int (*CheckFlights)[4],int Flen){// draw the shape of Laser in map
        int radius=6;
        int index;
        int xSign=(start[1]-end[1]>0) ? -1:1;
        
        int Rgb[]={218,218,168};
        double tail[2],head[2];
        double k=(1.0*start[0]-end[0])/(start[1]-end[1]);
        //printf("%f   %d   %d    %d   %d\n",k,start[0],end[0],start[1],end[1]);
        double pdk=-1/k;
        
        double r;
        int times=(int) ((sqrt(pow((start[0]-end[0]),2)+pow((start[1]-end[1]),2))-timeParam)/(radius*2+10));

        for (index=0;index<times;index++){
            r=timeParam+(radius*2+10)*index;
            tail[1]=xSign*(sqrt(pow(r,2)/(1+pow(k,2)))),tail[0]=tail[1]*k;
            
            head[1]=xSign*(sqrt(pow(r+radius*2,2)/(1+pow(k,2)))),head[0]=head[1]*k;
            drawOneOppoTriangle(map,tail,head,start,Rgb,pdk,radius,CheckFlights,Flen);
        }
    }
extern "C"{
    void drawLaser(int (*map)[5000*3],int (*start),int(*end),int timeParam){// draw the shape of Laser in map
        if (pow(start[1]-end[1],2)+pow(start[0]-end[0],2)<pow(200,2)){
            int radius=6;
            int index;
            int xSign=(start[1]-end[1]>0) ? -1:1;
            
            int Rgb[]={218,218,168};
            double tail[2],head[2];
            double k=(1.0*start[0]-end[0])/(start[1]-end[1]);
            //printf("%f   %d   %d    %d   %d\n",k,start[0],end[0],start[1],end[1]);
            double pdk=-1/k;
            
            double r;
            int times=(int) ((sqrt(pow((start[0]-end[0]),2)+pow((start[1]-end[1]),2))-timeParam)/(radius*2+10));

            for (index=0;index<times;index++){
                r=timeParam+(radius*2+10)*index;
                tail[1]=xSign*(sqrt(pow(r,2)/(1+pow(k,2)))),tail[0]=tail[1]*k;
                
                head[1]=xSign*(sqrt(pow(r+radius*2,2)/(1+pow(k,2)))),head[0]=head[1]*k;
                drawOneTriangle(map,tail,head,start,Rgb,pdk,radius);

                
            }

        }
        
    }
    void drawMapLine(int (*map)[5000*3]){
        int each,element,thi;
        int rgb[3]={34,52,59};
        int thick=4;
        for(int row=0;row<100;row++){
            for(each=0;each<5000;each++){
                for (element=0;element<3;element++){
                    for (thi=0;thi<thick;thi++){
                        map[row*100+thi][each*3+element]=rgb[element];
                    }
                    
                    
                };
            };
        };
        for(int col=0;col<50;col++){
            for(each=0;each<10000;each++){
                for (element=0;element<3;element++){
                    for (thi=0;thi<thick;thi++){
                        map[each][(col*100+thi)*3+element]=rgb[element];
                    };
                    
                };
            };
        };
    };
    
    void addVisibleArea(int (*map)[5000*3],int (*filghts)[4],int (*ScreenPosition),int i,int radius,int radiusOfScreen){
        if (abs(ScreenPosition[0]-filghts[i][1])<radiusOfScreen+220 && abs(ScreenPosition[1]-filghts[i][0])<radiusOfScreen+220){
            drawAVisible(map,filghts[i],radius);
        }
        

    }


    void drawFlights(int (*map)[5000*3],int (*MyFilghts)[4],int index,int *rgbSide,int *rgbBody,int (*ScreenPosition),int radiusOfScreen){
        if (abs(ScreenPosition[0]-MyFilghts[index][1])<radiusOfScreen+220 && abs(ScreenPosition[1]-MyFilghts[index][0])<radiusOfScreen+220){
            drawMyFlight(map,MyFilghts[index],rgbSide,rgbBody);
        }
        
    }
    void DrawMateFlights(int (*map)[5000*3],int (*mateFlights)[10],int *rgbSide,int *rgbBody,int timePara,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        int end[2];
        for (indexO=0;indexO<20;indexO++){
            if (mateFlights[indexO][4]!=0 && abs(ScreenPosition[0]-mateFlights[indexO][1])<radiusOfScreen+220 && abs(ScreenPosition[1]-mateFlights[indexO][0])<radiusOfScreen+220){
                drawMyFlight(map,mateFlights[indexO],rgbSide,rgbBody);
                if (mateFlights[indexO][5]==0 && mateFlights[indexO][6]==1){
                    end[0]=mateFlights[indexO][7];
                    end[1]=mateFlights[indexO][8];
                    drawLaser(map,mateFlights[indexO],end,timePara);
                }
            }
        }
    }
    void DrawMateScout(int (*map)[5000*3],int radius,int (*mateScouts)[6],int *rgbBody,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        for (indexO=0;indexO<10;indexO++){
            if (mateScouts[indexO][4]!=0 && abs(ScreenPosition[0]-mateScouts[indexO][1])<radiusOfScreen+radius && abs(ScreenPosition[1]-mateScouts[indexO][0])<radiusOfScreen+radius){
                drawAScout(map,mateScouts[indexO],rgbBody,radius);

            }

        }
    }
    void DrawMateTorpid(int (*map)[5000*3],int (*mateTorpids)[6],int *rgbBody,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        for (indexO=0;indexO<20;indexO++){
            if (mateTorpids[indexO][4]!=0 && abs(ScreenPosition[0]-mateTorpids[indexO][1])<radiusOfScreen+100 && abs(ScreenPosition[1]-mateTorpids[indexO][0])<radiusOfScreen+100){
                drawRectangle(map,mateTorpids[indexO],rgbBody);

            }

        }
    }


    void getThreePoint(int (*filghts),int Radius,double (*points)[2]){
        double x=955+195*filghts[1]/5000, y=410+390*filghts[0]/10000;
        double tail[2];
        double Rad=filghts[3]*3.14159/180;
        points[0][1]=y+(-sin(Rad)*Radius/1.5),points[0][0]=x+(cos(Rad)*Radius/1.5);
        tail[0]=sin(Rad)*(Radius/2),tail[1]=-cos(Rad)*(Radius/2);
        double k=(points[0][1]-y)/(points[0][0]-x);
        double pdk=-1/k;
        // points[1][0]=x+(sqrt(pow(Radius/2,2)/(pow(pdk,2)+1))+tail[1]),points[1][1]=y+sqrt(pow(Radius/2,2)/(pow(pdk,2)))*pdk+tail[0];
        // points[2][0]=x+(-sqrt(pow(Radius/2,2)/(pow(pdk,2)+1))+tail[1]),points[2][1]=y+(-sqrt(pow(Radius/2,2)/(pow(pdk,2)+1))*pdk+tail[0]);
        

        points[1][0]=sqrt(pow(Radius/2,2)/(pow(pdk,2)+1))+tail[1]+x,points[1][1]=(points[1][0]-tail[1]-x)*pdk+tail[0]+y;
        points[2][0]=-sqrt(pow(Radius/2,2)/(pow(pdk,2)+1))+tail[1]+x,points[2][1]=(points[2][0]-tail[1]-x)*pdk+tail[0]+y;
    }

    void DrawOpponentFlights(int (*map)[5000*3],int (*MyFilghts)[4],int MyLen,int (*opponentFlights)[10],int *rgbSide,int *rgbBody,int timePara,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        int end[2];
        for (indexO=0;indexO<20;indexO++){
            if (opponentFlights[indexO][4]!=0 && checkInRange(MyFilghts,opponentFlights[indexO][0],opponentFlights[indexO][1],MyLen,400) && abs(ScreenPosition[0]-opponentFlights[indexO][1])<radiusOfScreen+220 && abs(ScreenPosition[1]-opponentFlights[indexO][0])<radiusOfScreen+220){
                drawOppoFlight(map,opponentFlights[indexO],rgbSide,rgbBody,MyFilghts,MyLen);
                if (opponentFlights[indexO][5]==0 && opponentFlights[indexO][6]==1){
                    end[0]=opponentFlights[indexO][7];
                    end[1]=opponentFlights[indexO][8];
                    drawOppoLaser(map,opponentFlights[indexO],end,timePara,MyFilghts,MyLen);
                }
                
            }
        }
    }

    void DrawOpponentScout(int (*map)[5000*3],int (*MyFilghts)[4],int MyLen,int radius,int (*opponentScouts)[6],int *rgbBody,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        for (indexO=0;indexO<10;indexO++){
            if (opponentScouts[indexO][4]!=0 && checkInRange(MyFilghts,opponentScouts[indexO][0],opponentScouts[indexO][1],MyLen,250) && abs(ScreenPosition[0]-opponentScouts[indexO][1])<radiusOfScreen+radius && abs(ScreenPosition[1]-opponentScouts[indexO][0])<radiusOfScreen+radius){
                drawAOppoScout(map,opponentScouts[indexO],rgbBody,radius,MyFilghts,MyLen);

            }

        }
    }
    void DrawOpponentTorpid(int (*map)[5000*3],int (*MyFilghts)[4],int MyLen,int (*opponentTorpids)[6],int *rgbBody,int (*ScreenPosition),int radiusOfScreen){
        int indexO;
        for (indexO=0;indexO<20;indexO++){
            if (opponentTorpids[indexO][4]!=0 && checkInRange(MyFilghts,opponentTorpids[indexO][0],opponentTorpids[indexO][1],MyLen,250) && abs(ScreenPosition[0]-opponentTorpids[indexO][1])<radiusOfScreen+100 && abs(ScreenPosition[1]-opponentTorpids[indexO][0])<radiusOfScreen+100){
                drawOppoRectangle(map,opponentTorpids[indexO],rgbBody,MyFilghts,MyLen);

            }

        }
    }

    

    int CheckWhetherAttack(int (*opponentFlights)[10],double x,double y){ // return difference of position between target position and flight position
        int index;
        double distance;
        for (index=0;index<20;index++){
            //printf("%d \n",opponentFlights[index][4]);
            if (opponentFlights[index][4] !=0 && pow(opponentFlights[index][0]-y,2)+pow(opponentFlights[index][1]-x,2)<pow(30,2)   ){
                return index;
            }
        }
        return -1;
    }
    int CheckWhetherAttackTorpid(int (*opponentTorpid)[6],double x,double y){ // return difference of position between target position and torpid position
        int index;
        double distance;
        for (index=0;index<20;index++){
            
            if (opponentTorpid[index][4] !=0 && pow(opponentTorpid[index][0]-y,2)+pow(opponentTorpid[index][1]-x,2)<pow(30,2)   ){
                return index;
            }
        }
        return -1;
    }

    bool InRange(int (*filghts)[4],double y,double x,int MyLen,int radius){
        
        return checkInRange(filghts,(int)y,(int)x,MyLen,radius);
    }

    void Assgn(int (*newdata)[10],int (*opponentFlights)[10],int length){
        int index,head,tail;
        for(index=0;index<length;index++){
            for(head=0;head<10;head++){
                opponentFlights[index][head]=newdata[index][head];
            }
           
        }
        for(index=length;index<20;index++){

            opponentFlights[index][4]=0;
        }
    }
    void AssgnFlyer(int (*newdata)[6],int (*flyer)[6],int length,int orglen){
        int index,contain;
        for (index=0;index<length;index++){
            for(contain=0;contain<6;contain++){
                flyer[index][contain]=newdata[index][contain];
            }
            //flyer[index][4]=1;
        }
        for (index=length;index<orglen;index++){
            flyer[index][4]=0;
        }
    }


    void drawMyScout(int (*map)[5000*3],int (*MyScouts)[4],int MyLen,int *rgbBody,int radius,int (*ScreenPosition),int radiusOfScreen){
        int index;
        for(index=0;index<MyLen;index++){
            if (abs(ScreenPosition[0]-MyScouts[index][1])<radiusOfScreen+220 && abs(ScreenPosition[1]-MyScouts[index][0])<radiusOfScreen+220){
                drawAScout(map,MyScouts[index],rgbBody,radius);
            }
        }
    }

    void ReDraw(int (*map)[5000*3],int (*AllObjects),int radius){
        
        FillAVisible(map,AllObjects,radius);
        
        
    }

    void DrawTorpid(int (*map)[5000*3],int (*position),int *rgb){
        drawRectangle(map,position,rgb);
    }
}


