//vector.cpp

#include "vector.h"
#include <cmath>
#include <iostream>
using namespace std;


Vector:: Vector()
{
    x=0; y=0; z=0;
}


Vector:: Vector(float mx, float my, float mz)
{
    x=mx; y=my; z=mz;
}

Vector:: Vector(float coords[3])
{
    x=coords[0]; y=coords[1]; z=coords[2];
}

float Vector::length()
{
    return sqrtf(x*x+y*y+z*z);
}

void Vector::print()
{
    cout<<"<"<<x<<","<<y<<","<<z<<">"<<endl;
}

void Vector::input()
{
    cout<<"\nEnter x";
    cin>>x;
    cout<<"\nEnter y";
    cin>>y;
    cout<<"\nEnter z";
    cin>>z;
}

void Vector::normalize()
{
    int len=length();

    x/= len;
    y/= len;
    z/= len;
}

Vector Vector:: operator+(const Vector& v2)
{
    Vector v3;
    v3.x=x+v2.x;
    v3.y=y+v2.y;
    v3.z=z+v3.z;

    return v3;
}

Vector Vector:: operator-(const Vector& v2)
{
    Vector v3;
    v3.x=x-v2.x;
    v3.y=y-v2.y;
    v3.z=z-v2.z;

    return v3;
}

Vector Vector:: operator*(float scale)
{
    Vector v3;
    v3.x=x*scale;
    v3.y=y*scale;
    v3.z=z*scale;
    return v3;
}

float Vector:: operator*(const Vector&v2)
{
    float dot;
    dot=x*v2.x+y*v2.y+z*v2.z;

    return dot;
}

Vector:: operator float*()
{
    return &x;
}

bool Vector:: operator!=(const Vector& v2)
{
    return x!=v2.x || y!=v2.y || z!=v2.z;
}

bool Vector:: operator==(const Vector& v2)
{
    return x==v2.x && y==v2.y && z==v2.z;
}

std::istream& operator>>(std::istream& is, Vector& v2)//這地方Vector用const會有問題喔 & must be written
{
    cout<<"\nEnter x";
    cin >> v2.x;
    cout<<"\nEnter y";
    cin >> v2.y;
    cout<<"\nEnter z";
    cin >> v2.z;

    return is;
}

std::ostream& operator<<(std::ostream& os, const Vector& v2)
{
    cout<<"<"<<v2.x<<","<<v2.y<<","<<v2.z<<">\n";
    return os;
}
