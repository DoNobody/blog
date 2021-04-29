package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
)

func processTelnetCommand(str string, exitChan chan int) bool {
	if strings.HasPrefix(str, "@close") {
		fmt.Println("Session closed")
		return false
	} else if strings.HasPrefix(str, "@shutdown") {
		fmt.Println("server shutdown")
		exitChan <- 0
		return false
	}
	fmt.Println(str)
	return true
}

func handleSession(conn net.Conn, exitChan chan int) {

	// 开始处理会话
	fmt.Println("Session started:")

	reader := bufio.NewReader(conn)

	for {

		str, err := reader.ReadString('\n')

		if err == nil {
			str = strings.TrimSpace(str)

			if !processTelnetCommand(str, exitChan) {
				conn.Close()
				break
			}

			conn.Write([]byte(str + "\n"))
		} else {
			fmt.Println("Session Closed")
			conn.Close()
			break
		}
	}

}

func server(address string, exitchan chan int) {

	// 监听
	l, err := net.Listen("tcp", address)

	if err != nil {
		fmt.Println(err.Error())
		exitchan <- 1
	}

	fmt.Println("listen: " + address)
	defer l.Close()

	// 循环监听
	for {
		conn, err := l.Accept()
		if err != nil {
			fmt.Println(err.Error())
			continue
		}

		go handleSession(conn, exitchan)
	}

}
