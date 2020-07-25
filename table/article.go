package table

type Tag struct {
	TagID int `from:"id"`
	TagName string `from:"name"`
	CreateTime string `from:"create_time"`
}


type Article struct {
	ArticleID int `from:"id"`
	ArticleTitle string `from:"title"`
	CreateTime string `from:"create_time"`
	Article string `from:"article"`
	Abstract string `from:"abstract"`
}
