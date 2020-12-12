package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/jsonp", func(c *gin.Context) {
		c.JSONP(200, gin.H{"wechat": "flysnow_org"})
	})
	a := []string{"1", "2", "3"}
	r.GET("/secureJson", func(c *gin.Context) {
		c.SecureJSON(200, a)
	})
	r.Run(":8080")
}
