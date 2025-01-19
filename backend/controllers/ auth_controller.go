package controllers

import(
	"exchangeapp/models"
 
	"github.com/gin-gonic/gin"
)

func Register(ctx *gin.Context){
	var user models.User
	if err := ctx.ShouldBindJSON(&user); err != nil{
		ctx.JSON(http.StatusBadRequest, gin.H{"error":}) 
		return
	}
}	

