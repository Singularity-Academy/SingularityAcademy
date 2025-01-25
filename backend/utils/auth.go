package utils

import (
	"backend/config"
	"backend/models"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"github.com/dgrijalva/jwt-go"
	"github.com/sony/sonyflake"
	"math/big"
	"strings"
	"time"
)

func GenerateSnowflakeID() uint64 {
	sf := sonyflake.NewSonyflake(sonyflake.Settings{})
	id, err := sf.NextID()
	if err != nil {
		panic(err)
	}
	return id
}

const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

func generateSecureRandomString(length int) (string, error) {
	result := make([]byte, length)
	for i := range result {
		randomByte, err := rand.Int(rand.Reader, big.NewInt(int64(len(charset))))
		if err != nil {
			return "", err
		}
		result[i] = charset[randomByte.Int64()]
	}
	return string(result), nil
}

func Encrypt(passwd string) (string, error) {
	//生成salt
	salt, err := generateSecureRandomString(10)
	if err != nil {
		return "", err
	}
	return EncryptWithSalt(passwd, salt), nil
}

func EncryptWithSalt(passwd string, salt string) string {
	//一步加密
	hashPasswd := sha256.New()
	hashPasswd.Write([]byte(passwd))    // 写入数据
	hashedPasswd := hashPasswd.Sum(nil) // 计算哈希值

	//二步加密
	hashSalt := sha256.New()
	hashSalt.Write([]byte(salt + hex.EncodeToString(hashedPasswd))) // 写入数据
	hashedSalt := hashSalt.Sum(nil)                                 // 计算哈希值

	encryption := salt + "$" + hex.EncodeToString(hashedSalt)

	return encryption
}

func CheckPassword(passwd string, encryption string) bool {
	if strings.Count(encryption, "$") != 1 {
		return false
	}
	parts := strings.Split(encryption, "$")
	salt := parts[0]
	if EncryptWithSalt(passwd, salt) != encryption {
		return false
	}
	return true
}

var secretKey = []byte("AISAISAAA") // 你可以自定义你的密钥

type Claims struct {
	ID uint64 `json:"ID"`
	jwt.StandardClaims
}

func GenerateToken(id uint64) (string, error) {
	claims := Claims{
		ID: id,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(time.Hour * 24 * 30).Unix(), // 设置 token 过期时间，24 小时后过期
			Issuer:    "aiLearn",                                  // 设置签发人
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	// 使用密钥签名 Token
	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func ParseToken(tokenString string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		// 返回密钥用于验证
		return secretKey, nil
	})
	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, fmt.Errorf("invalid token")
	}
	return claims, nil
}

func FindUsersByID(id uint64) ([]models.User, error) {
	var users []models.User
	if err := config.DB.Where("id = ?", id).Find(&users).Error; err != nil {
		return users, err
	}
	return users, nil
}

func FindUsersByEmail(email string) ([]models.User, error) {
	var users []models.User
	if err := config.DB.Where("email = ?", email).Find(&users).Error; err != nil {
		return users, err
	}
	return users, nil
}
