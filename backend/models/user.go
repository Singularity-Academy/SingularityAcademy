package models

import "time"

type User struct {
	ID         uint64    `gorm:"primaryKey"` // Snowflake ID
	Username   string    `gorm:"unique;not null"`
	Email      string    `gorm:"unique;not null"`
	Password   string    `gorm:"not null"`
	RegisterAt time.Time `gorm:"autoCreateTime"`
}
