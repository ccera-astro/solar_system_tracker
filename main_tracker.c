/*
 * A piece of *EXAMMPLE* code to show how to call the solar_system_tracker.py program and read its
 * output until it has produced all that you have asked it to produce.
 */
#include <stdio.h>
#include <stdlib.h>
int main ()
{
	FILE *fp;
	char lines[2048];
	
	fp = popen("./solar_system_tracker.py --object 0332+54 --catalog --file PULSARS.EDB", "r");
	while (fgets (lines, sizeof(lines), fp) != NULL)
	{
		fprintf (stdout, "%s", lines);
		/*
		 * Depending on how your actual motion-control-hardware works
		 * You might stay in this loop, and every time you get an update
		 * from the Python script, command your motors, etc.
		 */
		 /*
		  * Alternatively, you might just command the tracker to produce a single line of output
		  *   giving you current Az/El, and your motion-control system can "take it from there".
		  */
	}
	pclose(fp);
	exit(0);
}
