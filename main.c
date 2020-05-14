//#include <iostream>
#include "stdio.h"
#include "string.h"
#include "stdlib.h"

#include "rapidjson/filereadstream.h"
#include "rapidjson/document.h"
#include <cstdio>

using namespace rapidjson;


//using namespace std;

#define     MAXSIZE     16*1024
#define     MAXPORT     1024

int CCOUNT = 0;

char cellsPrefix[1024][32];
/*
 "INV",
 "NAND",
 "NOR",
 "XNOR",
 "AND",
 "OR",
 "XOR",
 "AOI",
 "MUX",
 "CLKBUF",
 "FAX",
 "HAX",
 "DFFSR",
 "DFFPOS",
 "DFFNEG"
 };
 */

typedef struct {char type[32]; char name[32];char pins[32][32]; char nets[32][32]; unsigned pCnt;} GATE;
typedef struct {unsigned dir;char name[32];unsigned isBus;unsigned busSize;} PORT;

typedef enum {OUT=0, IN=1, CELL, FFD, FFQ} NODE_T;
typedef struct node_struct {NODE_T type; int fo_instances[32]; int fo_cnt; int instance;} NODE;
NODE graphNodes[MAXSIZE];

GATE circuitGates[MAXSIZE];
PORT circuitPorts[MAXPORT];

unsigned int gCount = 0, nCount = 0, ffCount = 0, portCount=0;
unsigned int nodeCount = 0;


Document doc;


/* Graph */
int buildGraph()
{
    int i;
    for(i=0;i<portCount;i++){
        graphNodes[nodeCount].type = (NODE_T) circuitPorts[i].dir;
        graphNodes[nodeCount].instance = i;
        nodeCount++;
    }
    for(i=0;i<gCount;i++){
        //graphNodes[nodeCount].type = (NODE_T) circuitPorts[i].dir;
        graphNodes[nodeCount].instance = i;
    }
    
    
}
/*
 int findFO(int gate, char *net, int list[]){
 int i, e;
 // fnd all cnnected cells to that net
 for(i=0; i<gCount; i++){
 if(i!=g){
 for(e=0; e<circuitGates[i].pCnt; e++){
 //if()
 }
 }
 }
 }
 
 */
//

int isCell(char *str)
{
    int i;
    for(i=0; i<CCOUNT; i++){
        if(strstr(str, cellsPrefix[i]))
            return 1;
    }
    return 0;
}

int getCell(FILE *fp, char *s)
{
    char buff[512];
    while(1) {
        if(!fgets(buff, 511, fp)) return 0;
        strtok(buff, "\n");
        strcat(s, buff);
        if(strchr(buff,';')) break;
    }
    return 1;
}

int getPinNet(char *s, char *n)
{
    char *p=strchr(s,'(');
    if(!*p) return 0;
    p++;
    while(*p!=')') *n++=*p++;
    *n='\0';
}

int getPinName(char *s, char *p)
{
    s++;
    while(*s!='(') *p++=*s++;
    *p='\0';
}

int getCellPins(char *s)
{
    char *p=s;
    char net[32], pin[32];
    while(p=strchr(p,'.')){
        getPinName(p, pin);
        getPinNet(p, net);
        strcpy(circuitGates[gCount].pins[circuitGates[gCount].pCnt],pin);
        strcpy(circuitGates[gCount].nets[circuitGates[gCount].pCnt++],net);
        //printf("pin: %s\n", net);
        p++;
    }
}

#define     ISW(s)     (*s==' ' || *s=='\t')
int parseNameAndType(char *s, char *nm, char *type)
{
    while(ISW(s)) s++;
    while(!ISW(s)) *type++=*s++;
    *type = '\0';
    while(ISW(s)) s++;
    while(!ISW(s)) *nm++=*s++;
    *nm = '\0';
}
/*
 int parseToken (char *s, char *tok, char *sep)
 {
 while(ISW(*s)) s++;
 while
 }*/
int parseRange(char *s, unsigned *r1, unsigned *r2){
    char num[32];
    char *p = num;
    s = strchr(s, '[');
    s++;
    while(*s!=':') *p++=*s++;
    *p = '\0';
    *r1=atoi(num);
    p = num;
    //s = strchr(s, ':');
    while(*s!=']') *p++=*s++;
    *p = '\0';
    *r2=atoi(num);
}


int parseGLV(FILE *fp)
{
    char line[512], tmp[512];
    char pin[32];
    char gname[32], gtype[32], pname[32];
    unsigned r1, r2, e, s;
    char *p, *l;
    
    while(fgets(line,511,fp)){
        if(isCell(line)) {
            strtok(line, "\n");
            if(getCell(fp, tmp))
                strcat(line, tmp);
            //printf("tmp: %s\n", tmp);
            //printf("found gate %s\n", line);
            parseNameAndType(line, gname, gtype);
            strcpy(circuitGates[gCount].type, gtype);
            strcpy(circuitGates[gCount].name, gname);
            getCellPins(line);
            gCount++;
            if(strstr(line,"DFF")) ffCount++;
            line[0]='\0';
            tmp[0]='\0';
        } else if(strstr(line, "wire")){
            // ignore internal wires inherited from the RTL
            if(!strstr(line, "]"))
                nCount++;
        } else if(strstr(line, "input")!=NULL || strstr(line, "output")!=NULL){
            if(strchr(line,'[')) {
                parseRange(line, &r1, &r2);
                if(r1>r2) {
                    s = r2;
                    e = r1;
                } else {
                    s = r1;
                    e = r2;
                }
                l = strchr(line, ']');
                l++;
                p=tmp;
                while(ISW(l)) l++;
                while(*l != ';') *p++=*l++;
                *p='\0';
                for(int i=s; i<=e; i++){
                    sprintf(circuitPorts[portCount].name, "%s[%d]",tmp,i);
                    if( strstr(line, "output"))
                        circuitPorts[portCount].dir = 0;
                    else
                        circuitPorts[portCount].dir = 1;
                    circuitPorts[portCount].isBus = 1;
                    portCount++;
                }
            }
            else {
                circuitPorts[portCount].isBus = 0;
                l = strstr(line, "put");
                //if(l==NULL)
                //l=line;
                l+=3;
                p=tmp;
                while(ISW(l)) l++;
                while(*l != ';') *p++=*l++;
                *p='\0';
                strcpy(circuitPorts[portCount].name, tmp);
                //circuitPorts[portCount].dir = 1;
                if( strstr(line, "output"))
                    circuitPorts[portCount].dir = 0;
                else
                    circuitPorts[portCount].dir = 1;
                portCount++;
            }
            
        }
    }
}

/* LIST */
typedef struct {int count; char items[256][32];} SLIST;
SLIST * lstNew(){
    
    SLIST *l = (SLIST *) malloc (sizeof(SLIST));
    l->count = 0;
    return l;
}
int lstAdd(SLIST *lst, char item[32]){
    strcpy(lst->items[lst->count], item);
    lst->count++;
    return (lst->count)-1;
}
int lstFind(SLIST *lst, char item[32]){
    int i;
    for(i=0; i<(lst->count); i++)
        if(!strcmp(lst->items[i],item)) return i;
    return -1;
}

int lstFindAdd(SLIST *lst, char item[32]){
    int x = lstFind(lst, item);
    if((x>-1))
        return x;
    else
        return lstAdd(lst,item);
}
/* */


#define     SCL_COUNT   256
int dumpGates()
{
    int i, e, f;
    int stats[SCL_COUNT], areas[SCL_COUNT];
    int area = 0;
    SLIST *cells;
    cells = lstNew();
    
    for(e=0; e<SCL_COUNT; e++) {stats[e]=0;areas[e]=0;}
    
    for(i=0; i<gCount; i++) {
        //printf("%d: %s\n", i, circuitGates[i].type);
        if(strstr( circuitGates[i].type,"_DLATCH_P_")){
            printf("Design Exception: The design infers a latch! Instatnce name: %s\n",  circuitGates[i].name);
            exit(-100);
        }
        f = lstFindAdd(cells, circuitGates[i].type);
        stats[f]++;
        areas[f] += doc["cells"][circuitGates[i].type]["area"].GetInt();
        area = area + doc["cells"][circuitGates[i].type]["area"].GetInt();
    }
    
    /*
     for(i=0; i<gCount; i++){
     //printf("JSON : %d\n", doc["cells"][circuitGates[i].type]["area"].GetInt());
     area = area + doc["cells"][circuitGates[i].type]["area"].GetInt();
     for(e=0; e<CCOUNT; e++)
     if(strstr(circuitGates[i].type,cellsPrefix[e])) {
     stats[e]++;
     break;
     }
     }
     */
    for(e=0; e<cells->count; e++) {
        printf("%s\tCount:%d, Area: %d\n", cells->items[e], stats[e], areas[e]);
    }
    printf("Total Cell Area: %d \n", area);
    printf("Equivalent NAND2x1 Gates count: %d\n",area/doc["cells"]["NAND2X1"]["area"].GetInt());
    
}

/*
 int getFO(int g, int fo[]){
 int foc = 0;
 int i;
 
 for(i=0; i<gCount; i++) {
 if(!strcmp(circuitGates[g].pins[]))
 }
 
 
 }
 */

int loadSCL(char *fn)
{
    int size;
    char tmp[32];
    FILE* fp = fopen(fn, "r"); // non-Windows use "r"
    fseek(fp, 0, SEEK_END); // seek to end of file
    size = ftell(fp); // get current file pointer
    fseek(fp, 0, SEEK_SET); // seek back to beginning of file
    
    char *readBuffer = (char *) malloc(size);
    
    FileReadStream is(fp, readBuffer, size);
    doc.ParseStream(is);
    
    //printf("\nJSON : %d\n", doc["cells"]["AND2X1"]["area"].GetInt());
    
    for (Value::ConstMemberIterator itr = doc["cells"].MemberBegin();
         itr != doc["cells"].MemberEnd(); ++itr)
    {
        strcpy(tmp, itr->name.GetString());
        if(!strcmp(tmp,"input")) continue;
        if(!strcmp(tmp,"output")) continue;
        if(!strcmp(tmp,"gnd")) continue;
        if(!strcmp(tmp,"vdd")) continue;
        strcpy(cellsPrefix[CCOUNT],tmp);
        CCOUNT++;
        
        printf("Type of member %s %s\n", itr->name.GetString(),cellsPrefix[CCOUNT-1]);
    }
    
    fclose(fp);
}

int main(int argc, char *argv[]) {
    FILE *fp;
    
    loadSCL("osu350.json");
    
    if((fp=fopen(argv[1],"r"))!=NULL){
        parseGLV(fp);
    }
    dumpGates();
    printf("total number of cells: %d (%d Flip FLops)\nTotal number of nets: %d\nTotal number of ports: %d\n", gCount, ffCount, nCount, portCount);
    
    fclose(fp);
    
    //loadSCL("osu350.json");
    
    return 0;
}
