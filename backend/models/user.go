package models

import "time"

type User struct {
	ID                uint64 `gorm:"primaryKey"`                 // Snowflake ID
	Username          string `gorm:"type:varchar(255);not null"` // 指定为 VARCHAR
	Email             string `gorm:"type:varchar(255);unique;not null"`
	Password          string `gorm:"type:varchar(255);not null"`
	IsVerified        bool
	VerificationToken string    `gorm:"type:varchar(10)"`
	RegisterAt        time.Time `gorm:"autoCreateTime"`
}
