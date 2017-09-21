#include "submit.h"

extern int ai_side;

int locx, locy; 

void init() {
	if (ai_side == 0) {
		locx = 2;
		locy = 10;
	} else {
		locx = 18;
		locy = 10;
	}
}

void GetUpdate(std::pair<int, int> location) {
	return;
}


bool temp = true;
std::pair<int, int> Action() {
	if (temp) {
		temp = false;
		Debug("GO~\n");
		return std::make_pair(locx, locy +2);
	} else {
		temp = true;
		Debug("Then I'm back~\n");
		return std::make_pair(locx, locy);
	}
}
