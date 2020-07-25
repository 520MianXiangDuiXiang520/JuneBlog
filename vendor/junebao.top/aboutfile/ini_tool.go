package aboutfile

import (
	"log"
	"path"
	"reflect"
	"runtime"
	"strconv"
	"strings"
)

func Load(iniPath, block string, s interface{}) {
	// 1. 读取ini文件
	_, currentfile, _, _ := runtime.Caller(1) // 忽略错误
	filename := path.Join(path.Dir(currentfile), iniPath)
	log.Println("ini Tool read [" + filename + "]")
	lines := ReadLines(filename)
	t := reflect.TypeOf(s)
	v := reflect.ValueOf(s)
	//v.Elem().Field(0).SetString("ssss")
	offset := 0
	for i, line := range lines {
		if line != "[" + block + "]" {
			continue
		}
		offset = i
	}
	lines = lines[offset:]
	for _, line := range lines {

		if len(line) <= 0 || string(line[0]) == "[" {
			continue
		}
		line = strings.Trim(line, "\n")
		line = strings.Trim(line, "\r")
		lr := strings.Split(line, "=")
		if len(lr) != 2 {
			panic("ini 格式错误")
		}
		for i := 0; i < t.Elem().NumField(); i++ {
			field := t.Elem().Field(i)
			s := field.Tag.Get("ini")
			if s == lr[0] {
				switch field.Type.Kind() {
				case reflect.String:
					v.Elem().Field(i).SetString(lr[1])
				case reflect.Int:
					a, b := strconv.Atoi(lr[1])
					if b != nil {
						panic("ini 格式错误")
					}
					v.Elem().Field(i).SetInt(int64(a))
				}
			}
		}
	}
}