package model

import (
	"time"

	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Name      string `json:"name"`
	Email     string `json:"email" gorm:"unique"`
	Password  string `json:"-"` // "-" means this field won't be included in JSON
	CreatedAt time.Time
	UpdatedAt time.Time
}
