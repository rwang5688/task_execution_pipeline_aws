all: bin/xvsa_scan

clean:
	rm -f bin/xvsa_scan

bin/xvsa_scan: xvsa_scan.cpp
	g++ -o xvsa_scan xvsa_scan.cpp
	mv xvsa_scan bin

