package main

import (
	"encoding/json"
	"os/exec"
	"strings"
	"flag"
	"fmt"
	"log"
	"os"
)

type settings struct {
	Build string `json:"build"`
	Run  string `json:"run"`
}

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

func runBuild() {
	file, _ := os.Open("./.anywhere/settings.json")
	defer file.Close()

	decoder := json.NewDecoder(file)

	// Technically bad practice and a struct should be used here.
	var defaultData settings

	// NEED to pass by reference! If not, how will it set the data dummy?
	decoder.Decode(&defaultData)

	trimmedString := strings.Replace(defaultData.Build, "--", "", -1)
	fmt.Printf("Command being executed: %s\n", trimmedString)
	
	cmd := exec.Command("cmd", "/C", trimmedString)
	output, err := cmd.CombinedOutput()

	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Output:\n", string(output))
	
}

func runRun() {
	file, _ := os.Open("./.anywhere/settings.json")
	defer file.Close()

	decoder := json.NewDecoder(file)

	// Technically bad practice and a struct should be used here.
	var defaultData settings

	// NEED to pass by reference! If not, how will it set the data dummy?
	decoder.Decode(&defaultData)

	trimmedString := strings.Replace(defaultData.Run, "--", "", -1)
	fmt.Printf("Command being executed: %s\n", trimmedString)
	
	cmd := exec.Command("cmd", "/C", trimmedString)
	output, err := cmd.CombinedOutput()

	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Output:\n", string(output))
}

func setBuild(command string) {
	readFile, _ := os.Open("./.anywhere/settings.json")
	defer readFile.Close()
	
	decoder := json.NewDecoder(readFile)
	
	// Technically bad practice and a struct should be used here.
	var defaultData settings
	
	// NEED to pass by reference! If not, how will it set the data dummy?
	decoder.Decode(&defaultData)
	
	defaultData.Build = command
	fmt.Printf("Unmarshaled Struct: %+v\n", defaultData)
	
	writeFile, _ := os.OpenFile("./.anywhere/settings.json", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0755)
	encoder := json.NewEncoder(writeFile)
	
	encoder.Encode(defaultData);
}

func setRun(command string) {
	readFile, _ := os.Open("./.anywhere/settings.json")
	defer readFile.Close()
	
	decoder := json.NewDecoder(readFile)
	
	// Technically bad practice and a struct should be used here.
	var defaultData settings
	
	// NEED to pass by reference! If not, how will it set the data dummy?
	decoder.Decode(&defaultData)
	
	defaultData.Run = command
	fmt.Printf("Unmarshaled Struct: %+v\n", defaultData)
	
	writeFile, _ := os.OpenFile("./.anywhere/settings.json", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0755)
	encoder := json.NewEncoder(writeFile)
	
	encoder.Encode(defaultData);
}

func main() {

	startUp()

	build := flag.String("build", "nil", "To edit the build command.")
	run := flag.String("run", "nil", "To edit the run command.")

	flag.Parse()

	// Runs when both are unset
	if (*build == "nil" && *run == "nil") {
		fmt.Println("--run = '' Sets the run command. Set to 'true' to run.")
		fmt.Println("--build = '' Sets the build command. Set to 'true' to run.")
	}

	// Runs when both are set
	if (*build != "nil" && *run != "nil") {
		fmt.Println("One at a time.")	
	}

	// TODO replace this with a generic run function and the argument is the key of the command that needs to be ran
	if (*build == "true") {
		runBuild()
	} else if (*run == "true") {
		runRun()
	} else if (*build != "true" && *run == "nil") {
		setBuild(*build)
	} else if (*run != "true" && *build =="nil") {
		setRun(*run)
	}
	
}