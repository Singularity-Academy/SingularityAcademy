package config

import (
	"github.com/spf13/viper"
	"log"
)

func LoadConfig() {
	// Enable reading from environment variables
	viper.AutomaticEnv()
	
	// Set environment variable mappings for database config
	viper.BindEnv("database.host", "DB_HOST")
	viper.BindEnv("database.port", "DB_PORT") 
	viper.BindEnv("database.user", "DB_USER")
	viper.BindEnv("database.password", "DB_PASSWORD")
	viper.BindEnv("database.name", "DB_NAME")
	
	viper.SetConfigName("config") // Config file name without extension
	viper.SetConfigType("yaml")   // Config file type
	viper.AddConfigPath("config") // Path to look for the config file in the current directory

	// Read the configuration (environment variables will override file values)
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("Error reading config file: %s", err)
	}
}
