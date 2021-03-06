#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <limits.h>

#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/extensions/HelperMacros.h>

#include "raat.hpp"
#include "raat-buffer.hpp"

#include "http-get-server.hpp"

static int s_called_last = 0;
static char s_last_url[16];
static char s_last_url_additional[16];

static void handler_function_1(char const * const url, char const * const url_additional)
{
    strncpy(s_last_url, url, 16);
    if (url_additional)
    {
        strncpy(s_last_url_additional, url_additional, 16);
    }
    s_called_last = 1;
}

static void handler_function_2(char const * const url, char const * const url_additional)
{
    strncpy(s_last_url, url, 16);
    if (url_additional)
    {
        strncpy(s_last_url_additional, url_additional, 16);
    }
    s_called_last = 2;
}

static void handler_function_3(char const * const url, char const * const url_additional)
{
    strncpy(s_last_url, url, 16);
    if (url_additional)
    {
        strncpy(s_last_url_additional, url_additional, 16);
    }
    s_called_last = 3;
}

static const http_get_handler s_handlers[] = 
{
    "/url1", handler_function_1,
    "/url2", handler_function_2,
    "/url3", handler_function_3,
    "/url4", NULL,
    NULL, NULL  
};

class RAATModuleHTTPGetServerTest : public CppUnit::TestFixture { 

    CPPUNIT_TEST_SUITE(RAATModuleHTTPGetServerTest);

    CPPUNIT_TEST(test_server_with_no_raat_handler_fn_does_nothing_when_passed_raat_commands);
    CPPUNIT_TEST(test_server_with_raat_handler_fn_correctly_passes_commands);
    CPPUNIT_TEST(test_server_with_no_handler_functions_does_nothing_when_passed_commands); 
    CPPUNIT_TEST(test_server_correctly_adds_response_code_headers_and_body);

    CPPUNIT_TEST_SUITE_END();

    void test_server_with_no_raat_handler_fn_does_nothing_when_passed_raat_commands()
    {
        HTTPGetServer test_server = HTTPGetServer(NULL);
        test_server.handle_req(s_handlers, "GET /device/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
        test_server.handle_req(s_handlers, "GET /param/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
        test_server.handle_req(s_handlers, "GET /module/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
    }

    void test_server_with_raat_handler_fn_correctly_passes_commands()
    {
        const raat_http_handlers raat_handlers = {handler_function_1, handler_function_2, handler_function_3};
        HTTPGetServer test_server = HTTPGetServer(&raat_handlers);
        test_server.handle_req(s_handlers, "GET /device/01/run");
        CPPUNIT_ASSERT_EQUAL(1, s_called_last);
        CPPUNIT_ASSERT_EQUAL(std::string("/device/01/run"), std::string(s_last_url));
        CPPUNIT_ASSERT_EQUAL(std::string("01/run"), std::string(s_last_url_additional));
        test_server.handle_req(s_handlers, "GET /param/01/run");
        CPPUNIT_ASSERT_EQUAL(2, s_called_last);
        CPPUNIT_ASSERT_EQUAL(std::string("/param/01/run"), std::string(s_last_url));
        CPPUNIT_ASSERT_EQUAL(std::string("01/run"), std::string(s_last_url_additional));
        test_server.handle_req(s_handlers, "GET /module/01/run");
        CPPUNIT_ASSERT_EQUAL(3, s_called_last);
        CPPUNIT_ASSERT_EQUAL(std::string("/module/01/run"), std::string(s_last_url));
        CPPUNIT_ASSERT_EQUAL(std::string("01/run"), std::string(s_last_url_additional));
    }

    void test_server_with_no_handler_functions_does_nothing_when_passed_commands()
    {
        HTTPGetServer test_server = HTTPGetServer(NULL);
        test_server.handle_req(NULL, "GET /device/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
        test_server.handle_req(NULL, "GET /param/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
        test_server.handle_req(NULL, "GET /module/01/run");
        CPPUNIT_ASSERT_EQUAL(0, s_called_last);
    }

    void test_server_correctly_adds_response_code_headers_and_body()
    {
        HTTPGetServer test_server = HTTPGetServer(NULL);
        test_server.set_response_code("200 OK");
        test_server.set_header("Access-Control-Allow-Origin", "*");
        test_server.set_header("X-Clacks-Overhead", "GNU Terry Pratchett");
        test_server.finish_headers();
        test_server.add_body("Lorem ipsum dolor sit amet, consectetur adipiscing elit.");
        char * pResponse = test_server.get_response();
        CPPUNIT_ASSERT_EQUAL(
            std::string("HTTP/1.1 200 OK\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "X-Clacks-Overhead: GNU Terry Pratchett\r\n\r\n"
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
            std::string(pResponse));
    }


public:
    void setUp()
    {
        s_called_last = 0;
        s_last_url[0] = '\0';
        s_last_url_additional[0] = '\0';
    }
};

CPPUNIT_TEST_SUITE_REGISTRATION(RAATModuleHTTPGetServerTest);
