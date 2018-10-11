#ifndef _ADL_ONESHOT_TIMER_H_
#define _ADL_ONESHOT_TIMER_H_

class ADLOneShotTimer
{
public:
	ADLOneShotTimer(uint16_t period);
	void start();
	bool check();
	void reset();
	bool check_and_reset();
	bool check_and_restart();
	bool is_running();
private:
	unsigned long m_start;
	uint16_t m_period;
	bool m_running;
};

#endif