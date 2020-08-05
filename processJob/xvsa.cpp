#include <iostream>
using namespace std;

int main(int argc, char **argv)
{
    // print arguments
    cout << "Starting xvsa (mock) ..." << endl;
    cout << "Number of arguments: " << argc << endl;
    for (int i = 0; i < argc; i++) {
        cout << i << ": " << argv[i] << endl;
    }
    cout.flush();

    // simulate workload when we have at least 4 arguments
    if (argc >= 4) {
        // simulate scan by executing "ls" command on .i file list
        string command1 = "ls";
        for (int i = 1; i < argc-2; i++) {
            command1.append(" " + string(argv[i]));
        }
        cout << "Executing: " << command1 << endl;
        cout.flush();
        system(command1.c_str());

        // invoke callback function with logFile
        string callback = argv[argc-2];
        string logFile = argv[argc-1];
        string command2 = "python " + callback + " " + logFile;
        cout << "Executing: " << command2 << endl;
        system(command2.c_str());
    }

    // done
    return 0;
}
