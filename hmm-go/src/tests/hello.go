package main

import (
	"fmt"
	"hmm"
)

func main() {
	fmt.Printf("Hello, world.\n")
	p := []float64{2.0, 3.0, 5.0}
	fmt.Println(hmm.Normalize(p))
}
