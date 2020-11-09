#include "blake2.h"
#include <iostream>
#include <string>
#include <stdint.h>

int main()
{
	std::string instr = "2011 9 59162.00 P  0.147674 0.001601  0.293396 0.001276  P-0.1744419 0.0005017                 P  -112.730    0.322    -7.323    0.160";

	uint8_t out[4];
	blake2b((void*)out, 4, instr.c_str(), instr.size(), NULL, 0);

	for (int i = 0; i < 4; i++) {
		printf("%02x", out[i]);
	}
	printf("\n");

	return 0;
}