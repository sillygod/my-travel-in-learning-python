//vector.h


#ifndef ELEMENTS_H
#define ELEMENTS_H

// #include <iostream>

//because this class data is often used, put the data in the public

class Vector
{

    // friend std::istream& operator>>(std::istream& is, Vector& v2);
    // friend std::ostream& operator<<(std::ostream& os,const Vector& v2);

public:
    //data member
    float x;
    float y;
    float z;
    //constructor
    Vector();
    Vector(float mx,float my,float mz);
    Vector(float coords[3]);
    //function

    float length();
    //void print();
    //void input();
    void normalize();

    //operator overloading

    Vector operator+(const Vector& v2); //through testing, the parameter just could have one or zero. in this case
    Vector operator-(const Vector& v2);
    Vector operator*(float scale);
    float operator*(const Vector& v2);

    bool operator!=(const Vector& v2);
    bool operator==(const Vector& v2);

    // operator float*(); // type convert operator overloading


    // >> << overloading. due to cin and cout is an object be defined,
    // like this ex:cout.operator<<(varable);
    // if we want to use cout<< vector; ps: vector self define data
    // we must use the no-member function(also friend function) as follow




};


// in order to use swig for wrapping vector as module,
// we need to avoid use some identifier that swig
// doesn't support.
//
// std::istream& operator>>(std::istream& is, Vector& v2);
// std::ostream& operator<<(std::ostream& os,const Vector& v2);


class Circle
{
public:

    Circle();
    Circle(float x, float y, float r);

    bool isCollision(Circle& c);


    Vector pos;
    float radius;
};


#endif
