#include "submit.h"

extern int ai_side;
std::string ai_name="Heart Breaker 1.1";

int locx, locy; 
int d = 0;

void init() {
	std::cout<<"�����������˵ķḻ���";
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
	std::cout<<"�����������˵ķḻ���";
	return;
}


bool temp = true;
bool once = true;

std::pair<int, int> Action() {
	std::cout<<"�����������˵ķḻ���";
	return  std::make_pair(-1,-1);
}
