package main

import (
	"flag"
	"fmt"
)

func main() {

	name := flag.String("name", "World", "To change the string outputted.")
	
	flag.Parse()

    fmt.Printf("Hello %s!", *name)
}