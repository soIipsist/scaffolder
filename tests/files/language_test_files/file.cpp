#include <iostream>
#include <string>

class MyClass {
public:
    // Constructor
    MyClass() {
        std::cout << "Constructor called" << std::endl;
    }

    // Destructor
    ~MyClass() {
        std::cout << "Destructor called" << std::endl;
    }

    // Member function
    void memberFunction() {
        std::cout << "Member function called" << std::endl;
    }

    // Overloaded function
    void overloadedFunction(int a) {
        std::cout << "Overloaded function with int called: " << a << std::endl;
    }

    void overloadedFunction(double a) {
        std::cout << "Overloaded function with double called: " << a << std::endl;
    }

    // Static member function
    static void staticFunction() {
        std::cout << "Static function called" << std::endl;
    }

    // Const member function
    void constFunction() const {
        std::cout << "Const function called" << std::endl;
    }

protected:
    // Protected member function
    void protectedFunction() {
        std::cout << "Protected function called" << std::endl;
    }

private:
    // Private member function
    void privateFunction() {
        std::cout << "Private function called" << std::endl;
    }

    // Virtual function
    virtual void virtualFunction() {
        std::cout << "Virtual function called" << std::endl;
    }
};

// Template function
template <typename T>
T templateFunction(T a, T b) {
    return a + b;
}

// Free function
void freeFunction() {
    std::cout << "Free function called" << std::endl;
}

int main() {
    MyClass obj;
    obj.memberFunction();
    obj.overloadedFunction(10);
    obj.overloadedFunction(3.14);
    MyClass::staticFunction();
    obj.constFunction();
    freeFunction();

    std::cout << "Template function: " << templateFunction(1, 2) << std::endl;

    return 0;
}
