package courses

import (
	"backend/code"
	"backend/models"
	"backend/response"
	"fmt"
	"github.com/gin-gonic/gin"
	"os"
	"path/filepath"
	"strconv"
)

func Materials(context *gin.Context) {
	// 获取上传的文件
	file, err := context.FormFile("materials")
	if err != nil {
		fmt.Println("upload")
		response.Fail(context, code.Errors.FailedToUploadFile)
		return
	}

	// 创建保存文件的目录
	dir := "./materials"
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err := os.MkdirAll(dir, os.ModePerm)
		if err != nil {
			response.Fail(context, code.Errors.FailedToCreateFolder)
			return
		}
	}

	user, _ := context.Get("user")

	// 保存文件到服务器
	filePath := filepath.Join(dir, strconv.FormatUint(user.(models.User).ID, 10)+"$"+file.Filename)
	if err := context.SaveUploadedFile(file, filePath); err != nil {
		response.Fail(context, code.Errors.FailedToSaveFolder)
		return
	}

	// 响应成功
	response.Success(context, gin.H{
		"message": "uploadSuccessfully",
		"file":    strconv.FormatUint(user.(models.User).ID, 10) + "$" + file.Filename,
	})
}
