#pragma once
class test_c {
 public:
   test_c();
   ~test_c();
   void set_log();
   void (test_c::*p1)(void);
   //int (test_c::*p2)(int, char*);
};

//extern void set_log();

