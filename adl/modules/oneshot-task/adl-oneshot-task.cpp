/*
 * Arduino Includes
 */

#include <Arduino.h>

/*
 * C/C++ Includes
 */

#include <stdlib.h>
#include <stdint.h>

/*
 * ADL Includes
 */

#include "device.h"
#include "parameter.h"
#include "adl-oneshot-timer.h"
#include "adl-oneshot-task.h"

/*
 * Class Functions
 */

ADLOneShotTask::ADLOneShotTask(uint16_t period, OneShotTask pfnTask) :
	m_timer(period), m_pfn_task(pfnTask), m_p_data(NULL)
{

}

ADLOneShotTask::ADLOneShotTask(uint16_t period, OneShotTask pfnTask, void * pData) : 
	m_timer(period), m_pfn_task(pfnTask), m_p_data(pData)
{
	
}

void ADLOneShotTask::start()
{
	m_timer.start();
}

bool ADLOneShotTask::run()
{
	if (m_timer.check_and_reset())
	{
		if (m_pfn_task)
		{
			m_pfn_task(m_p_data);
		}
	}
	return m_timer.is_running();
}

bool ADLOneShotTask::is_running()
{
	return m_timer.is_running();
}

void ADLOneShotTask::reset()
{
	m_timer.reset();
}