package config

import (
	"log"

	"github.com/spf13/viper"
	
)

type Config struct {
	App struct {
		Name string
		Port string
	}

	Database struct {
		Dsn 	 string
		MaxIdleConns int
		MaxOpenConns int
		Host     string
		Port     string
		User     string
		Password string
		Name     string
	}
}

var AppConfig *Config

func InitConfig() {
	viper.SetConfigName("config") // File name without extension
	viper.SetConfigType("yml")    // File type
	viper.AddConfigPath("./config") // Directory containing the config file

	// Read the config file
	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file: %v", err)
	}

	AppConfig = &Config{} // Initialize AppConfig

	// Unmarshal the config into the Config struct
	if err := viper.Unmarshal(AppConfig); err != nil {
		log.Fatalf("Unable to decode config into struct: %v", err)
	}

	initDB()
}