package tools

import (
	"database/sql"
	"errors"
	"fmt"
	"junebao.top/aboutfile"
	"strconv"
)

type mysqlStruct struct {
	DbName   string `ini:"dbname"`
	User     string `ini:"user"`
	Port     int    `ini:"port"`
	Password string `ini:"password"`
	Ip       string `ini:"ip"`
}

func Conn(filePath, iniBlock string) (*sql.DB, error) {
	var ms mysqlStruct
	aboutfile.Load(filePath, iniBlock, &ms)
	fmt.Println(ms.Port)
	conn := ms.User+ ":" + ms.Password+"@tcp(" + ms.Ip+
		":" + strconv.Itoa(ms.Port) + ")/" + ms.DbName +"?charset=utf8&parseTime=True&loc=Local"
	fmt.Println(conn)
	DB, err := sql.Open("mysql", conn)
	if err == nil {
		return DB, nil
	} else {
		return nil, errors.New("数据库连接错误")
	}
}
