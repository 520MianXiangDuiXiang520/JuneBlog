package base

import "strconv"

func StringToInt(str string) int {
	result, err := strconv.Atoi(str)
	if err != nil {
		panic("转换失败")
	}
	return result
}

func IntToString(i int) string {
	return strconv.Itoa(i)
}
