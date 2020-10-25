#include <iostream>
using namespace std;

#define SUCCESS 0
#define ERROR -1


/**
 * Execute workload
 */
int execute_workload(int argc, char **argv)
{
    // simulate workload by executing "ls" on preprocess directory
    string command = "ls";
    command.append(" " + string(argv[1]) + "/*/preprocess");

    // debug: print command
    cout << "Executing: " << command << endl;
    cout.flush();

    // execute command
    system(command.c_str());

    return SUCCESS;
}

/**
 * xvsa_scan mock
 */
int main(int argc, char **argv)
{
    // print arguments
    cout << "Starting xvsa_scan mock ..." << endl;
    cout << "Number of arguments: " << argc << endl;
    for (int i = 0; i < argc; i++) {
        cout << i << ": " << argv[i] << endl;
    }
    cout.flush();

    // exit if not enough arguments
    if (argc < 2) {
        cerr << "xvsa_scan: Not enough arguments. Exit." << endl;
        exit (ERROR);
    }

    // execute workload
    int success = execute_workload(argc, argv);
    if (success != SUCCESS) {
        cerr << "execute_workload failed.  Exit." << endl;
        exit(ERROR);
    }

    return SUCCESS;
}

