#include <iostream>
using namespace std;

#define SUCCESS 0
#define ERROR -1


/**
 * Execute workload
 */
int execute_workload(int argc, char **argv)
{
    // simulate workload by executing "ls" cmd on .i file list
    string command = "ls";
    for (int i = 1; i < argc-2; i++) {
        command.append(" " + string(argv[i]));
    }
    cout << "Executing: " << command << endl;
    cout.flush();
    system(command.c_str());

    return SUCCESS;
}


/**
 * Execute callback
 */
int execute_callback(string callback, string jobId, string jobStatus, string jobLogfile)
{
    string command = "python3 " + callback + " " + jobId + " " + jobStatus + " " + jobLogfile;
    cout << "Executing: " << command << endl;
    cout.flush();
    system(command.c_str());

    return SUCCESS;
}


/**
 * xvsa mock
 */
int main(int argc, char **argv)
{
    // print arguments
    cout << "Starting xvsa mock ..." << endl;
    cout << "Number of arguments: " << argc << endl;
    for (int i = 0; i < argc; i++) {
        cout << i << ": " << argv[i] << endl;
    }
    cout.flush();

    // execute workload if we have enough arguments
    if (argc >= 4) {
        int success = SUCCESS;

        // execute workload
        success = execute_workload(argc, argv);
        if (success != SUCCESS) {
            cerr << "execute_workload failed.  Exit." << endl;
            exit(ERROR);
        }

        // execute callback function with jobId, jobStatus, jobLogfile
        string callback = argv[argc-2];
        string jobId = argv[argc-1];
        string jobStatus = "completed";
        string jobLogfile = "log.v";
        success = execute_callback(callback, jobId, jobStatus, jobLogfile);
        if (success != SUCCESS) {
            cerr << "execute_callback failed.  Exit." << endl;
            exit(ERROR);
        }
    }

    return SUCCESS;
}

