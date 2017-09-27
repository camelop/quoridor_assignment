#include "submit.h"

extern int ai_side;
std::string ai_name="Your_ai_name_here";

int locx, locy; 
int d = 0;

void init() {
	/* Your code here */
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
	/* Your code here */
}


bool temp = true;

std::pair<int, int> Action() {
	/* Your code here */
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
