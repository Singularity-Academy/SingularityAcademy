package courses

import (
	"backend/models"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
)

func Materials(context *gin.Context) {
	// 获取上传的文件
	file, err := context.FormFile("materials")
	if err != nil {
		fmt.Println("upload")
		context.JSON(http.StatusBadRequest, gin.H{"error": "failedToUploadFile", "detail": err.Error()})
		return
	}

	// 创建保存文件的目录
	dir := "./materials"
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err := os.MkdirAll(dir, os.ModePerm)
		if err != nil {
			context.JSON(http.StatusInternalServerError, gin.H{"error": "failedToCreateFolder", "detail": err.Error()})
			return
		}
	}

	user, _ := context.Get("user")

	// 保存文件到服务器
	filePath := filepath.Join(dir, strconv.FormatUint(user.(models.User).ID, 10)+"$"+file.Filename)
	if err := context.SaveUploadedFile(file, filePath); err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"error": "failedToSaveFolder", "detail": err.Error()})
		return
	}

	// 响应成功
	context.JSON(http.StatusOK, gin.H{
		"message": "uploadSuccessfully",
		"file":    strconv.FormatUint(user.(models.User).ID, 10) + "$" + file.Filename,
	})
}
