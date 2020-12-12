package main

import (
	"bytes"
	"container/list"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"reflect"
	"strconv"
	"time"

	"github.com/labstack/echo"
	"github.com/pkg/profile"
	"github.com/skip2/go-qrcode"
)

func main() {

	// 性能测试
	stopper := profile.Start(profile.CPUProfile, profile.ProfilePath("."))

	// defer stopper.Stop()

	/* 这是我的第一个简单的程序 */
	fmt.Println("Hello, World!")
	var i, j int
	for i = 2; i < 100; i++ {
		for j = 2; j <= (i / j); j++ {
			if i%j == 0 {
				break
			}
		}
		if j > (i / j) {
			fmt.Printf("%d  是素数\n", i)
		}
	}

	// func
	nextNumber := getSequence()
	for i := 0; i <= 3; i++ {
		fmt.Println(nextNumber())
	}

	// method
	var c1 Circle
	c1.radius = 10
	fmt.Printf("半径：%3f, 面积：%3f \n", c1.radius, c1.getArea())

	// multi-dimensional-arrays
	var array1 = [5][3]int{{0, 0}, {1, 1}, {2, 2}, {3, 3}, {4, 4}}
	var ptr [5][3]*int
	for i := 0; i < 5; i++ {
		for j := range array1[i] {
			//    fmt.Println(j)
			ptr[i][j] = &array1[i][j]
			fmt.Printf("array1[%d][%d]:%d : %d\n", i, j, ptr[i][j], *ptr[i][j])
		}
	}

	// go slice
	numbers := []int{0, 1, 2, 3, 4, 5, 6, 7, 8}

	printSlice(numbers)

	fmt.Println("numbers ==", numbers)

	/* 打印子切片从索引1(包含) 到索引4(不包含)*/
	fmt.Println("numbers[1:4] ==", numbers[1:4])

	/* 默认下限为 0*/
	fmt.Println("numbers[:3] ==", numbers[:3])

	/* 默认上限为 len(s)*/
	fmt.Println("numbers[4:] ==", numbers[4:])

	numbers = append(numbers, 10)

	fmt.Println("numbers[:] append 10 ==", numbers[:])

	fmt.Println("numbers[:len(numbers)] ==", numbers[:len(numbers)])
	fmt.Println("numbers[:cap(numbers)] ==", numbers[:cap(numbers)])

	numbers1 := make([]int, 0, 5)
	printSlice(numbers1)

	/* 打印子切片从索引  0(包含) 到索引 2(不包含) */
	number2 := numbers[:2]
	printSlice(number2)

	/* 打印子切片从索引 2(包含) 到索引 5(不包含) */
	number3 := numbers[2:5]
	printSlice(number3)

	// go-recursion
	for i := 0; i < 10; i++ {
		go fmt.Printf("%s\t", strconv.Itoa(fibonacci(i)))
	}
	fmt.Println()

	// go-interface
	var phone Phone
	phone = new(XiaomiPhone)
	phone.call()

	phone = new(IPhone)
	phone.call()

	// channel
	s := []int{7, 4, 9, 8, -1, 5}
	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)
	go sum(s, c)
	x, y := <-c, <-c
	fmt.Println("channel: ", s[:len(s)/2], s[len(s)/2:])
	fmt.Println("channel: ", x, y, x+y)

	// channel2
	c = make(chan int, 10)
	go fibonacci2(cap(c), c)
	for i := range c {
		fmt.Println("fib2: ", i)
	}

	// 类型别名，主要用于底层编程，或者反射
	var a Vehicle

	// 指定调用特定的show方法
	a.FakeBrand.Show()

	// 获取a的类型反射
	// 需要import reflect 包
	ta := reflect.TypeOf(a)

	// 遍历a的成员
	for i := 0; i < ta.NumField(); i++ {

		// 获取成员信息
		f := ta.Field(i)

		// 打印成员的字段名和类型
		fmt.Printf("FileName: %v, FiledType: %v \n", f.Name, f.Type.Name())
	}
	// 测试list，链表
	l := list.New()
	l.PushBack("one")
	l.PushFront("two")
	three := l.PushBack("three")
	l.InsertAfter("four", three)
	l.InsertBefore("five", three)
	l.Remove(three)
	// 遍历读取
	for i := l.Front(); i != nil; i = i.Next() {
		fmt.Println("List:", i.Value)
	}

	// 快速排序
	qsort(s, 0, len(s)-1)
	fmt.Println(s)

	// 生成二维码
	qrcode.WriteFile("https://donobody.github.io/blog/#/", qrcode.Medium, 256, "./golang_qrcode.png")

	// 引入外部包，验证go mod 依赖
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})

	// 自己构建一个telnet服务
	exitChan := make(chan int)

	// 将服务器并发运行
	go server("127.0.0.1:7001", exitChan)

	go e.Start(":1323")
	//e.Logger.Fatal(e.Start(":1323"))

	// 写入文件
	info := []Website{{"Golang", "http://c.biancheng.net/golang/", []string{"http://c.biancheng.net/cplus/", "http://c.biancheng.net/linux_tutorial/"}}, {"Java", "http://c.biancheng.net/java/", []string{"http://c.biancheng.net/socket/", "http://c.biancheng.net/python/"}}}

	filePtr, err := os.Create("info.json")
	if err != nil {
		fmt.Println("创建文件失败", err.Error())
		return
	}

	defer filePtr.Close()

	encoder := json.NewEncoder(filePtr)

	err = encoder.Encode(info)
	if err != nil {
		fmt.Println("编码错误", err.Error())
	} else {
		fmt.Println("编码成功")
	}

	// 读取json文件
	filePtr1, err := os.Open("./info.json")
	if err != nil {
		fmt.Println("打开文件失败", err.Error())
	}

	// defer filePtr1.Close()

	var info1 []Website

	decoder := json.NewDecoder(filePtr1)
	err = decoder.Decode(&info1)
	info2, err := json.Marshal(info1)
	if err != nil {
		fmt.Println("String转化失败", err.Error())
	}
	var str bytes.Buffer
	err = json.Indent(&str, info2, "", "  ")

	if err != nil {
		fmt.Println("解码失败", err.Error())
	} else {
		fmt.Println("解码成功")
		fmt.Println(info1)
		fmt.Println(str.String())
	}

	// 通道阻塞, 等待接收返回值
	code := <-exitChan

	// 中断退出，退出前保存性能报告
	stopper.Stop()
	// 标记程序返回值并退出
	os.Exit(code)

}

func getSequence() func() int {
	i := 0
	return func() int {
		i++
		return i
	}
}

//Circle ⭕️
type Circle struct {
	radius float64
}

func (c Circle) getArea() float64 {
	return 3.14 * c.radius * c.radius
}

func printSlice(x []int) {
	fmt.Printf("len=%d cap=%d slice=%v\n", len(x), cap(x), x)
}

// 采用递归的方式，缺点是会重复计算n-1的阶乘次
func fibonacci(n int) int {
	if n < 2 {
		return n
	}
	time.Sleep(10 * time.Millisecond)
	return fibonacci(n-1) + fibonacci(n-2)
}

// 使用channel方式进行返回
func fibonacci2(n int, ch chan int) {
	x, y := 0, 1
	for i := 0; i < n; i++ {
		ch <- x
		x, y = y, x+y
	}
	close(ch)
}

/* interfaces */

//Phone base interface
type Phone interface {
	call()
}

//XiaomiPhone 小米手机
type XiaomiPhone struct {
}

func (xiaomiPhone XiaomiPhone) call() {
	fmt.Println("I am XiaomiPhone")
}

//IPhone iphone 手机
type IPhone struct {
}

func (iphone IPhone) call() {
	fmt.Println("I am IPhone")
}

// channel
func sum(s []int, ch chan int) {
	sum := 0
	for _, s := range s {
		sum += s
	}
	ch <- sum // 将sum的值放到ch中
}

// 类型别名，主要用于底层编程，或者反射

//Brand 定义商标结构
type Brand struct {
}

//Show 为商标结果体添加一个Show方法
func (b Brand) Show() {
}

//FakeBrand 为Brand定义一个别名FakeBrand
type FakeBrand = Brand

//Vehicle 定义车辆结构体
type Vehicle struct {
	// 潜入两个结构体
	FakeBrand
	Brand
}

// 写入json文件的结构体

// Website ...
type Website struct {
	Name   string `xml:"name,attr"`
	URL    string
	Course []string
}
