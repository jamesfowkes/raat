#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/extensions/HelperMacros.h>

#include "raat.hpp"
#include "protocol.hpp"

class SimpleProtocolTest : public CppUnit::TestFixture { 

    CPPUNIT_TEST_SUITE(SimpleProtocolTest);
    CPPUNIT_TEST(testValidBoardDeviceCommandIsProcessed);
    CPPUNIT_TEST_SUITE_END();

  
    void testValidBoardDeviceCommandIsProcessed() {
        char valid_command[] = "D00R";
        ProtocolHandler s_protocol_handler;

        s_protocol_handler.process(valid_command);

        CPPUNIT_ASSERT_EQUAL(0, s_protocol_handler.last_address);
        CPPUNIT_ASSERT_EQUAL(ADDRESS_TYPE_DEVICE, s_protocol_handler.last_address_type);
        CPPUNIT_ASSERT_EQUAL(std::string("R"), std::string(s_protocol_handler.command));
  }
};

int main()
{
   CppUnit::TextUi::TestRunner runner;
   
   CPPUNIT_TEST_SUITE_REGISTRATION( SimpleProtocolTest );

   CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();

   runner.addTest( registry.makeTest() );
   runner.run();

   return 0;
}
