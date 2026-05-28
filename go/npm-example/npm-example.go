package main

import (
	"fmt"
	"os/exec"
)

func main() {
	// Create the command (name, args...)
	cmd := exec.Command("npm", "help")

	out, err := cmd.Output()
	// Run and capture standard output
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Output:\n", string(out))
}
