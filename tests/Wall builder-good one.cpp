#include "submit.h"
#include <unistd.h>

extern int ai_side;
std::string ai_name="Test: Wall builder-good one";

int locx, locy; 
int d = 0;

bool temp = true;
const int S = 10;
int px[S] = {0,0,3,3,3,3,17,17,17,17};
int py[S] = {0,0,2,6,12,16,2,6,12,16};
int nw = 0;

void init() {
	if (ai_side == 0) {
		locx = 2;
		locy = 10;
		d = 2;
	} else {
		locx = 18;
		locy = 10;
		d = -2;
	}
	locx+=d;
	px[1]=locx;
	py[1]=locy;
}

void GetUpdate(std::pair<int, int> location) {
	return;
}



std::pair<int, int> Action() {
	if (nw<S){
		nw+=1;
		return std::make_pair(px[nw], py[nw]);
	}
	if (temp) {
		temp = false;
		Debug("GO~\n");
		locx+=d;
		return std::make_pair(locx, locy);
	} else {
		temp = true;
		Debug("Then I'm back~\n");
		locx+=d;
		return std::make_pair(locx, locy);
	}
}
