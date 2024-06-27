using System;

class Program
{
    // Regular method
    static int Add(int a, int b)
    {
        return a + b;
    }

    // Lambda function assigned to a variable
    static Func<int, int, int> Multiply = (x, y) => x * y;

    // Anonymous method
    static Func<int, int> Square = delegate (int num)
    {
        return num * num;
    };

    static void Main()
    {
        // Usage of each function
        Console.WriteLine("Addition result: " + Add(3, 5));
        Console.WriteLine("Multiplication result: " + Multiply(4, 6));
        Console.WriteLine("Square result: " + Square(9));
    }
}
