// File.js

const simpleLambda = () => console.log("Simple lambda function");

const add = (a, b) => a + b;

const multiply = (x, y) => {
    return x * y;
};

const square = num => num * num;

const complexLambda = (name, age) => {
    let info = `Name: ${name}, Age: ${age}`;
    return info;
};

const arrowFunction = (param1, param2) => param1 * param2;

const asyncLambda = async () => {
    let result = await fetch('https://api.example.com/data');
    return result.json();
};

const decoratedLambda = (callback) => {
    console.log("Before executing callback");
    callback();
};

const noParamsLambda = () => "No parameters";

// Exporting a lambda function
export const exportedLambda = (value) => value * 2;

// Lambda function with default parameter
const defaultParamLambda = (x = 10) => x * 2;

// Lambda function using let
let letLambda = (x) => x + 1;

console.log(simpleLambda());
console.log(add(3, 5));
console.log(multiply(4, 6));
console.log(square(9));
console.log(complexLambda("Alice", 30));
console.log(arrowFunction(3, 4));
console.log(asyncLambda());
console.log(decoratedLambda(() => console.log("Executing callback")));
console.log(noParamsLambda());
console.log(exportedLambda(5));
console.log(defaultParamLambda());
console.log(letLambda(7));
