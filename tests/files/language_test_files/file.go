// File.go

package main

import (
	"fmt"
)

func testcount(x int) int {
	if x == 11 {
		return 0
	}
	fmt.Println(x)
	return testcount(x + 1)
}

func main() {
	// Lambda functions assigned to variables
	add := func(a, b int) int {
		return a + b
	}

	multiply := func(x, y int) int {
		return x * y
	}

	square := func(num int) int {
		return num * num
	}

	// Anonymous lambda function
	func(x int) {
		fmt.Println("Anonymous lambda function with argument:", x)
	}(5)

	fmt.Println("Addition result:", add(3, 5))
	fmt.Println("Multiplication result:", multiply(4, 6))
	fmt.Println("Square result:", square(9))
}
