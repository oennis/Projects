EXE = peer
CFLAGS = -Wall
CXXFLAGS = -Wall
LDLIBS =
CC = gcc
CXX = g++

.PHONY: all
all: $(EXE)

# Implicit rules defined by Make, but you can redefine if needed
#
#peer: peer-to-peer.c
#	$(CC) $(CFLAGS) peer-to-peer.c $(LDLIBS) -o peer
#
# OR
#
peer: peer-to-peer.cpp
	$(CXX) $(CXXFLAGS) peer-to-peer.cpp $(LDLIBS) -o peer

.PHONY: clean
clean:
	rm -f $(EXE)
