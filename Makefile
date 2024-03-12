INCLUDE = include
SOURCE = src
STANDARD = -std=c++20
SRC_FILES = $(wildcard $(SOURCE)/*.cpp)
INCLUDE_FILES = $(wildcard $(INCLUDE)/*.hpp)
CPP_FLAGS = $(STANDARD)
MAIN = evoguessr

all:
	g++ $(CPP_FLAGS) $(SRC_FILES) -I $(INCLUDE_FILES) -o $(MAIN)