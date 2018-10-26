#ifndef _PROTOCOL_H_
#define _PROTOCOL_H_

class ProtocolHandler: public ProtocolHandlerBase
{
public:
    ProtocolHandler();
    ADDRESS_TYPE process(char * simple);
    void write_reply(char * buffer, char const * const reply, uint8_t reply_length);
};

#endif
