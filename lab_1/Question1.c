#include <stdio.h>
#include <unistd.h>

int main(){
	pid_t pid;

	pid = fork();
	if (pid < 0){
		// fork has failed
		printf("Fork Failed! \n");
	}
	
	else if (pid == 0){
		//child process is created
		printf("Child process created...\n");
		printf("\tPPID = %d\n", getppid()); // print parent pid for this child.
		printf("\tPID = %d\n", getpid()); // print pid of this child process.
		printf("Child Process sleep for 5 sec...\n");
		sleep(5); //sleep child process for 5 sec before termination
		printf("Child process terminated.\n");
	}
	
	else{
		//parent process is created
		wait(); //wait for child proccess to terminate
		printf("Parent Process...\n");
		printf("\tPID = %d\n", getpid()); // print pid for this process
		printf("Parent Process sleep for 5 sec...\n");
		sleep(5); //sleep parent processs for 5 sec before termination
		printf("Parent process terminated.\n");
	}
}