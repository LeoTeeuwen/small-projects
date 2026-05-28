package main

import (
	"encoding/json"
	"fmt"
	"os"
	"log"
)

func startUp() {
	// Check and create the folder if it does not exist
	if _, err := os.Stat("./.anywhere"); os.IsNotExist(err) {
		fmt.Println("Folder does not exist!")
		err := os.Mkdir("./.anywhere", 0755)
		
		if err != nil {
			log.Fatal(err)
		} else {
			fmt.Println("Created folder!")
		}
	}

	if _, err := os.Stat("./.anywhere/settings.json"); os.IsNotExist(err) {
		fmt.Println("Settings json does not exist!")

		defaultData := map[string]interface{}{
			"run": "npm --help",
			"build": "npm --help",
		}

		file, _ := os.Create("./.anywhere/settings.json")
		defer file.Close()

		encoder := json.NewEncoder(file)
		
		encoder.Encode(defaultData)
		if _, err := os.Stat("./.anywhere/settings.json"); os.IsNotExist(err) {
			fmt.Println("Created settings.json and its contents!")
		}
	}
}

func main() {

	startUp()

}