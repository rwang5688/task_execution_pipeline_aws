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
 * Invoke callback
 */
int invoke_callback(string callback, string jobId, string jobStatus, string logFile)
{
    string command = "python " + callback + " " + jobId + " " + jobStatus + " " + logFile;
    cout << "Executing: " << command << endl;
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

    // simulate workload when we have at least 4 arguments
    if (argc >= 4) {
        int success = SUCCESS;
        success = execute_workload(argc, argv);
        if (success != SUCCESS) {
            cerr << "execute_workload failed.  Exit." << endl;
            exit(ERROR);
        }

        // invoke callback function with jobId and logFile
        string callback = argv[argc-2];
        string jobId = argv[argc-1];
        string jobStatus = "complete";
        string logFile = "log.v";
        success = invoke_callback(callback, jobId, jobStatus, logFile);
        if (success != SUCCESS) {
            cerr << "invoke_callback failed.  Exit." << endl;
            exit(ERROR);
        }
    }

    return SUCCESS;
}

