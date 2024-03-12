#include <iostream>
#include <string>
#include <stdlib.h>

int main(int argc, char** argv) {
    for (int argi = 0; argi < argc; argi++) {
        std::cout << std::string(argv[argi]) << std::endl;
    }
    return 0;
}