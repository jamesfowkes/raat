#ifndef _INTEGER_PARAM_H_
#define _INTEGER_PARAM_H_

typedef enum _eRGB
{
    eR, eG, eB
} eRGB;


class RGBParam : public ParameterBase
{
public:
    RGBParam(int16_t limit, int16_t r_default, int16_t g_default, int16_t b_default, bool clip_on_out_of_range=true);
    void setup();
    void reset();
    int command_handler(char const * const command, char * reply);
    
    bool set(uint16_t rgb[3]);
    bool set(uint16_t r, uint16_t g, uint16_t b);
    uint16_t get(eRGB index);
    void get(uint16_t rgb[3]);
private:
    LimitedRangeInt m_rgb[3];
    int16_t m_defaults[3];
    bool m_clip;
};

#endif
