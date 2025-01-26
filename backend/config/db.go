package config

import (
	"fmt"
	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
)

var DB *gorm.DB

func LoadConfig() {
	viper.SetConfigName("config")  // Config file name without extension
	viper.SetConfigType("yaml")    // Config file type
	viper.AddConfigPath("/config") // Path to look for the config file in the current directory

	// Read the configuration
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("Error reading config file: %s", err)
	}
}

func ConnectDatabase() {
	// Load configuration
	LoadConfig()

	// Extract database details from the configuration
	user := viper.GetString("database.user")
	password := viper.GetString("database.password")
	host := viper.GetString("database.host")
	port := viper.GetInt("database.port")
	dbName := viper.GetString("database.name")
	charset := viper.GetString("database.charset")
	parseTime := viper.GetBool("database.parseTime")
	loc := viper.GetString("database.loc")

	// Construct the DSN
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=%s&parseTime=%t&loc=%s",
		user, password, host, port, dbName, charset, parseTime, loc,
	)

	// Open the database connection
	database, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database: " + err.Error())
	}
	DB = database
}

//func ConnectDatabase() {
//	dsn := "AIS:AISAISAAA@tcp(156.238.229.162:3306)/test1?charset=utf8mb4&parseTime=True&loc=Local"
//	database, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
//	if err != nil {
//		panic("Failed to connect to database: " + err.Error())
//	}
//	DB = database
//}
