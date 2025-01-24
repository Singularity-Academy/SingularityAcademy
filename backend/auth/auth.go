package auth

import (
	"log"
	"os"
)

var Logger = log.New(os.Stdout, "[auth] ", log.LstdFlags|log.Lmicroseconds|log.Lshortfile)
