package config

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
	"time"
	"backend/global"
)

func initDB(){
	Dsn := AppConfig.Database.Dsn
	db, err := gorm.Open(mysql.Open(Dsn), &gorm.Config{})
	
	if err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}

	sqlDB, err := db.DB()

	sqlDB.SetMaxIdleConns(AppConfig.Database.MaxIdleConns)
	sqlDB.SetMaxOpenConns(AppConfig.Database.MaxOpenConns)
	sqlDB.SetConnMaxLifetime(time.Hour)
	
	if err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}

// 	// Migrate the schema
	global.Db = db 
}

