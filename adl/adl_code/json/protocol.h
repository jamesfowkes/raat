class ProtocolHandler: public ProtocolHandlerBase
{
public:
	ProtocolHandler();
	bool process(char * json);
	void write_reply(char * buffer, char const * const reply, uint8_t reply_length);

private:
	char m_command_copy[16];

};
