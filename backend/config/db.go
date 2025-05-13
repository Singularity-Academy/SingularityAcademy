package config

import (
	"fmt"
	"log"

	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

// The original MySQL connection function
func ConnectDatabaseMySQL() {
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
		log.Printf("[error] failed to initialize database, got error %v", err)
		panic("Failed to connect to database: " + err.Error())
	}
	DB = database
}

// Use SQLite instead which doesn't require authentication
func ConnectDatabase() {
	database, err := gorm.Open(sqlite.Open("sa_database.db"), &gorm.Config{})
	if err != nil {
		log.Printf("[error] failed to initialize SQLite database, got error %v", err)
		panic("Failed to connect to SQLite database: " + err.Error())
	}
	log.Printf("Successfully connected to SQLite database")
	DB = database
}
