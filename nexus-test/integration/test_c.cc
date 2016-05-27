#include "test_c.h"
#include "base/logging.h"

test_c::test_c(){}

test_c::~test_c() {}

void test_c::set_log() {
//void set_log(){
   DVLOG(0)<<"[popexizhi] test_c::set_log......";
//   printf("[popexizhi] test_c::set_log......");
}
