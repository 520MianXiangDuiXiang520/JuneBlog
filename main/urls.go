package main

import "github.com/gin-gonic/gin"

func Routes(engine *gin.Engine) {
	// 文章标签路由组
	tagsGroup := engine.Group("api/go/juneBlog/tags")
	// 文章详情路由组
	articleGroup := engine.Group("api/go/juneBlog/article")

	// 获取所有标签
	tagsGroup.GET("/list", getAllTags)

	// 获取文章详情接口
	articleGroup.GET("/detail/:article_id", getArticleDetail)
	// 获取文章标签接口
	articleGroup.GET("/tag", getTags)
}
