#include "submit.h"
#include <unistd.h>

extern int ai_side;
std::string ai_name="Artificial Idiot V2p";

int locx, locy; 
int d = 0;

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
}

void GetUpdate(std::pair<int, int> location) {
	return;
}


bool temp = true;
bool once = true;

std::pair<int, int> Action() {
	usleep(500);
	if (once){
		once= false;
		locy-=2;
		return std::make_pair(locx, locy);
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
