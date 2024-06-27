#include <stdio.h>

// Function with no return value and no parameters
void simpleFunction() {
    printf("This is a simple function.\n");
}

// Function with an integer return type and no parameters
int returnIntFunction() {
    return 42;
}

// Function with parameters
float add(float a, float b) {
    return a + b;
}

// Function with multiple parameters of different types
double complexFunction(int a, double b, char c) {
    return a + b + c;
}

// Static function
static void staticFunction() {
    printf("This is a static function.\n");
}

// Function with pointer parameters
void pointerFunction(int *p) {
    *p = 10;
}

// Function returning a pointer
char* returnPointerFunction() {
    return "Hello, World!";
}

// Function with array parameters
void arrayFunction(int arr[], int size) {
    for(int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Function with a pointer to a function as a parameter
void callbackFunction(void (*callback)(int)) {
    callback(100);
}

// Function with const parameters
void constFunction(const char *str) {
    printf("Const parameter: %s\n", str);
}

// Inline function
inline int inlineFunction(int x) {
    return x * x;
}

// Function declaration (prototype)
void prototypeFunction();

int main() {
    simpleFunction();
    printf("Return int: %d\n", returnIntFunction());
    printf("Add: %f\n", add(3.5, 4.5));
    printf("Complex: %f\n", complexFunction(2, 3.5, 'A'));

    staticFunction();

    int num = 0;
    pointerFunction(&num);
    printf("Pointer function: %d\n", num);

    printf("Return pointer: %s\n", returnPointerFunction());

    int arr[] = {1, 2, 3, 4, 5};
    arrayFunction(arr, 5);

    callbackFunction([](int val) { printf("Callback value: %d\n", val); });

    constFunction("Test const");

    printf("Inline function: %d\n", inlineFunction(5));

    prototypeFunction();

    return 0;
}

// Function definition for the prototype
void prototypeFunction() {
    printf("This is a prototype function.\n");
}
