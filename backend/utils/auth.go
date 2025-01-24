package utils

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"github.com/sony/sonyflake"
	"math/big"
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
	hashSalt.Write([]byte(salt + passwd)) // 写入数据
	hashedSalt := hashSalt.Sum(nil)       // 计算哈希值

	var encryption string = hex.EncodeToString(hashedSalt) + "$" + hex.EncodeToString(hashedPasswd)

	return encryption
}
