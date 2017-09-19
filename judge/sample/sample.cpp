#include "submit.h"

extern int ai_side;

std::pair<int, int> loc;

int main() {
	SubmitInit();
	if (ai_side == 0) {
		loc = std::make_pair(2, 10);
		while (true) {
			std::pair<int, int> temp;
			Post(std::make_pair(4, 10));
			Debug("I go four ten.\n");
			temp = GetUpdate();
			Post(std::make_pair(2, 10));
			Debug("Then I'm back~\n");
			temp = GetUpdate();
		}
	}
	else {
		loc = std::make_pair(18, 10);
		while (true) {
			std::pair<int, int> temp;
			temp = GetUpdate();
			Post(std::make_pair(16, 10));
			Debug("I go sixteen ten.\n");
			temp = GetUpdate();
			Post(std::make_pair(18, 10));
			Debug("Then I'm back~\n");
		}
	}
	return 0;
}
