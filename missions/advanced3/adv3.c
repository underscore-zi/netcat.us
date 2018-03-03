#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int askQuestion(int i, int x, int y, char op)
{
int answer;
int solution;

printf("#%d: %d %c %d?\n", i, x, op, y);

fflush(stdout);

scanf("%d", &answer);

switch(op)
{
case '+':
solution = x + y;
break;

case '-':
solution = x - y;
break;
}

if(answer != solution)
{
printf("Hey! You are not a robot! No humans allowed!!!! %d\n", solution);
return -1;
}

return 0;
}

int runChallenge()
{
int i = 0;

char garbage[2];

printf("ADVANCED 3 :: ROBOT CITY OVERRUN\n");
printf("-\n");
printf("The humans have tasked you with infiltrating robot city and exploiting their identification system, however the robots have a defense mechanism - you must solve many math problems to verify you're a functioning robot.\n\n");

void *sysAddr = &system;

fflush(stdout);

for(i = 0; i < 100; i++)
{
int x;
int y;
int operation;
int solution;
int answer;

x = rand() % 100000;
y = rand() % 100000;
operation = rand() % 2;

switch(operation)
{
case 0:
if(askQuestion(i, x, y, '+') < 0)
return -1;

break;

case 1:
if(askQuestion(i, x, y, '-') < 0)
return -1;

break;
}
}

printf("Congratulations! You're not a human.\n");
printf("**************************************************\n\n");

fflush(stdout);
return 0;
}

void printWelcome(char *name)
{
printf("Welcome to robot city, %s\n", name);
}

void identify()
{
void (*funcPtr)(char *) = &printWelcome;
char name[16];
char garbage[8];
int nameLength;
size_t nameSize;
int n;

char *nameBuff = name;

char *binsh = "/bin/sh";

memset(name, 0, sizeof(name));

printf("Identify yourself robot!\n\n");

printf("Enter your name: \n");

fflush(stdout);
while ( getchar() != '\n' );
if(fgets(nameBuff, 64, stdin))
{
(*funcPtr)(nameBuff);
}
}

void sys(char* cmd) {
volatile int i = 1;
system(cmd);
if(i) return;
asm __volatile__ (".byte 0x2f; .byte 0x62; .byte 0x69; .byte 0x6e; .byte 0x2f; .byte 0x73; .byte 0x68; .byte 0x00; .byte 0x00;");
}

int main()
{
srand((unsigned int)time(NULL));
setvbuf(stdout, NULL, _IONBF, 0);
sys("/bin/false"); //Keep the compiler from optimizing the dead code out
if(runChallenge() == 0)
identify();
exit(0);
}

