package controllers

import (
	"backend/code"
	"backend/response"
	"io/ioutil"
	"path/filepath"
	"strconv"

	"github.com/gin-gonic/gin"
)

func GetUserMaterials(c *gin.Context) {
	userIdStr := c.Param("userId")
	userId, err := strconv.ParseUint(userIdStr, 10, 64)
	if err != nil {
		response.FailCode(c, code.Errors.BadRequest.Code, "Invalid user ID")
		return
	}

	// 构建用户材料的目录路径
	dir := "./materials"
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		response.FailCode(c, code.Errors.InternalError.Code, "Failed to read materials directory")
		return
	}

	var userFiles []gin.H
	for _, file := range files {
		if !file.IsDir() {
			// 检查文件名是否以 "userId$" 开头
			prefix := strconv.FormatUint(userId, 10) + "$"
			if filepath.HasPrefix(file.Name(), prefix) {
				// 读取文件内容
				content, err := ioutil.ReadFile(filepath.Join(dir, file.Name()))
				if err != nil {
					continue
				}
				userFiles = append(userFiles, gin.H{
					"filename": file.Name(),
					"content":  string(content),
				})
			}
		}
	}

	response.Success(c, gin.H{
		"files": userFiles,
	})
}
