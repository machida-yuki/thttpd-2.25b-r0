#include <string.h> 
#include <sys/time.h> 
#include <time.h> 

#if 1
int gettimeofday(struct timeval *tv, struct timezone *tz)
{
        struct timespec tp;

	memset(&tp,0,sizeof(tp));

	clock_gettime(CLOCK_MONOTONIC,&tp);
	
	tv->tv_sec=tp.tv_sec;
	tv->tv_usec=0;
	
	return 0;
}


time_t time( time_t *t )
{
        struct timespec tp;

	memset(&tp,0,sizeof(tp));

	clock_gettime(CLOCK_MONOTONIC,&tp);
	
	if(t!=NULL){
		*t=tp.tv_sec;
	}

	return tp.tv_sec;
}

#endif
