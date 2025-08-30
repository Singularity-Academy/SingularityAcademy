package config

import (
	"github.com/spf13/viper"
	"log"
)

func LoadConfig() {
	viper.SetConfigName("config") // Config file name without extension
	viper.SetConfigType("yaml")   // Config file type
	viper.AddConfigPath("config") // Path to look for the config file in the current directory

	// Read the configuration
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("Error reading config file: %s", err)
	}
}
