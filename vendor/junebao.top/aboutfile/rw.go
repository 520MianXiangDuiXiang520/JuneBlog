package aboutfile

import (
	"bufio"
	"io"
	"os"
)

func ReadLines(filePath string) []string {
	result := make([]string, 0)
	f, err := os.Open(filePath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	rd := bufio.NewReader(f)
	for {
		line, err := rd.ReadString('\n') //以'\n'为结束符读入一行
		if err != nil || io.EOF == err {
			break
		}
		result = append(result, line)
	}
	return result
}


