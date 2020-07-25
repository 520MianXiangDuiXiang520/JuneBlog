package aboutweb

import "github.com/gin-gonic/gin"

func Resp500(context *gin.Context) {
	RespCode(500, "服务异常", nil, context)
}

func Resp300(context *gin.Context) {
	RespCode(300, "请求参数异常", nil, context)
}

func RespCode(code int, msg string, data interface{}, context *gin.Context) {
	context.JSON(200, map[string]interface{}{
		"code": code,
		"msg": msg,
		"data": data,
	})
}
