#include "raat.hpp"

#include "analog-input.hpp"

AnalogInput::AnalogInput(int pin)
{
    m_pin = pin;
}

void AnalogInput::reset() {}
void AnalogInput::tick() {}

void AnalogInput::setup()
{
    pinMode(m_pin, INPUT);
}

unsigned int AnalogInput::reading()
{
    return analogRead(m_pin);
}

uint16_t AnalogInput::command_handler(char const * const command, char * reply)
{
    (void)command;
    unsigned int value = analogRead(m_pin);
    sprintf(reply, "%u", value);
    return strlen(reply);
}
