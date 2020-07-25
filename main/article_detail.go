package main

import (
	"database/sql"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
	"junebao/aboutweb"
	"junebao/base"
	"juneblog/table"
	"juneblog/tools"
	"log"
)



var DB *sql.DB

func dbInit() {
	filePath := "../setting.ini"
	DB, _ = tools.Conn(filePath, "mysql")
}

func getNextArticle(articleID int) (int, string) {
	var nextArticleID int
	var nextArticleTitle string
	rows := DB.QueryRow("SELECT 序号, 标题 FROM article WHERE `序号`>?", articleID)
	err := rows.Scan(&nextArticleID, &nextArticleTitle)
	if err != nil {
		return -1, "无"
	}
	return nextArticleID, nextArticleTitle
}

func getPreArticle(articleID int) (int, string) {
 	var preArticleID int
 	var preArticleTitle string
	rows := DB.QueryRow("SELECT 序号, 标题 FROM article WHERE `序号`<?", articleID)
	err := rows.Scan(&preArticleID, &preArticleTitle)
	if err != nil {
		return -1, "无"
	}
	return preArticleID, preArticleTitle
}

func getArticleDetail(context *gin.Context) {
	articleId := context.Param("article_id")
	articleIntId := base.StringToInt(articleId)
	nextID, nextTitle := getNextArticle(articleIntId)
	preID, preTitle := getPreArticle(articleIntId)
	var article table.Article
	rows:= DB.QueryRow("SELECT * FROM article WHERE `序号`=?", articleId)
	if err := rows.Scan(&article.ArticleID, &article.ArticleTitle, &article.CreateTime,
		&article.Abstract, &article.Article); err != nil {
		aboutweb.Resp500(context)
	}
	aboutweb.RespCode(200, "ok", map[string]interface{}{
		"article": article,
		"next": map[string]interface{}{
			"id": nextID,
			"title": nextTitle,
		},
		"previous": map[string]interface{}{
			"id": preID,
			"title":preTitle,
		},

	}, context)

}

func getTags(context *gin.Context) {
	articleID:= context.Query("article_id")
	articleIntID := base.StringToInt(articleID)
	if articleIntID <= 0 {
		aboutweb.Resp300(context)
	} else {
		rows, err := DB.Query("SELECT 序号, 标签名, 创建时间 FROM article_tags, tags WHERE article_id = ?" +
			" AND article_tags.article_id = tags.序号", articleID)
		if err != nil {
			aboutweb.Resp500(context)
		} else {
			tags := make([]table.Tag, 0)
			for rows.Next() {
				var tag table.Tag
				_ = rows.Scan(&tag.TagID, &tag.TagName, &tag.CreateTime)
				tags = append(tags, tag)
			}
			aboutweb.RespCode(200, "ok", tags, context)
		}
	}
}

func getAllTags(context *gin.Context) {
	rows, err := DB.Query("SELECT tags_id, tags.`标签名`, 创建时间, COUNT(*) FROM article_tags, tags  WHERE tags_id = 序号 GROUP BY tags_id;")
	if err != nil {
		log.Println(err)
		aboutweb.Resp500(context)
	} else {
		result := make([]map[string]interface{}, 0)
		for rows.Next() {
			var tag table.Tag
			var articleNum int
			_ = rows.Scan(&tag.TagID, &tag.TagName, &tag.CreateTime, &articleNum)
			result = append(result, map[string]interface{}{
				"TagID": tag.TagID,
				"TagName": tag.TagName,
				"CreateTime": tag.CreateTime,
				"Num": articleNum,
			})
		}
		aboutweb.RespCode(200, "ok", result, context)
	}
}

func main() {
	dbInit()
	defer DB.Close()
	engine := gin.Default()
	Routes(engine)
	_ = engine.Run()
}
