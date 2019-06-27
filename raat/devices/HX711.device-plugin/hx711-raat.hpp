#ifndef _HX711RAAT_H_
#define _HX711RAAT_H_

class HX711RAAT : public DeviceBase
{
public:
    HX711RAAT(uint8_t dout_pin, uint8_t sck_pin, bool tare_at_boot);
    void setup();
    void reset();
    void tick();
    uint16_t command_handler(char const * const command, char * reply);
    bool get_scaled(long& reading);
    long get_scaled(void);
    bool get_raw(long& reading);
    long get_raw(void);
    void tare(void);
private:

	HX711 m_loadcell;
    uint8_t m_dout_pin;
    uint8_t m_sck_pin;
    
    bool m_tare_at_boot;
};

#endif
