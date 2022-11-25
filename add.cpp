#include <iostream>

int Add(int a, int b) 
{
    return a+b;
}

extern "C" {
    int My_Add(int a, int b)
    {
        return Add(a);
    }
}
