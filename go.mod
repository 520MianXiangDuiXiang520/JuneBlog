module juneblog

go 1.14

require (
	github.com/gin-gonic/gin v1.6.3
	github.com/go-sql-driver/mysql v1.5.0
	junebao.top/aboutfile v0.0.0
	junebao.top/aboutweb v0.0.0
	junebao.top/base v0.0.0
)

replace (
	junebao.top/aboutfile v0.0.0 => ../junebao.top/aboutfile
	junebao.top/aboutweb v0.0.0 => ../junebao.top/aboutweb
	junebao.top/base v0.0.0 => ../junebao.top/base
)
