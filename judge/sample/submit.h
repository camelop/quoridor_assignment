#include <iostream>
#include <string>

/******************************************/
std::string ai_name = "Artificial Idiot V0";
/******************************************/

int ai_side; // 0 -> up and 1 -> down

void SubmitInit() {
	std::cin >> ai_side;
	std::cout << ai_name << '\n';
	std::cout.flush();
}

std::pair<int, int> GetUpdate() {
	int a, b;
	std::cin >> a >> b;
	return std::make_pair(a, b);
}

void Post(std::pair<int, int> loc) {
	std::cout << loc.first << ' ' << loc.second << '\n';
	std::cout.flush();
}

void Debug(std::string message) {
	std::cerr << message;
	std::cerr.flush();
}
