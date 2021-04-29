package main

import (
	"io/ioutil"
	"net/http"
	"testing"

	"github.com/gin-gonic/gin"
)

func startJSONServer() {
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

func TestJsonp(t *testing.T) {
	go startJSONServer()
	resp, err := http.Get("http://127.0.0.1:8080/jsonp")
	if err != nil {
		t.Fail()
		t.Log(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fail()
		t.Log(err)
	}
	t.Log(string(body))

	resp1, err := http.Get("http://127.0.0.1:8080/secureJson")
	if err != nil {
		t.Fail()
		t.Log(err)
	}
	defer resp1.Body.Close()
	body1, err := ioutil.ReadAll(resp1.Body)
	if err != nil {
		t.Fail()
		t.Log(err)
	}
	t.Log(string(body1))
}
