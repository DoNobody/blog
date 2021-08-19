package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"time"

	"github.com/robfig/cron"

	"github.com/Shopify/sarama"
	cluster "github.com/bsm/sarama-cluster"
	jsoniter "github.com/json-iterator/go"
	"github.com/sdbaiguanghe/glog"
)

var (
	//snb的,名称起的特殊而已
	recivebrokers = []string{"kafka01.tp.base.phd2.jianlc.jlc:9091", "kafka02.tp.base.phd2.jianlc.jlc:9091"}
	recivetopics  = "radarlog"
	reciveGroupID = "radar"

	//数据组
	dataSendBrokers = []string{"kafka01.tp.base.phd2.jianlc.jlc:9091", "kafka02.tp.base.phd2.jianlc.jlc:9091"}
	dataSendTopic   = "logmonitor"

	lastDiffTime int64 = 0
	maxDiffTime  int64 = 5 * 60 * 1000
)

func consumer() {
	// init (custom) config, enable errors and notifications
	config := cluster.NewConfig()
	config.Consumer.Return.Errors = true
	config.Group.Return.Notifications = true

	// init consumer
	topics := []string{recivetopics}
	consumer, err := cluster.NewConsumer(recivebrokers, reciveGroupID, topics, config)
	if err != nil {
		panic(err)
	}
	defer consumer.Close()

	// trap SIGINT to trigger a shutdown.
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, os.Interrupt)

	// consume errors
	go func() {
		for err := range consumer.Errors() {
			log.Printf("Error: %s\n", err.Error())
		}
	}()

	// consume notifications
	go func() {
		for ntf := range consumer.Notifications() {
			log.Printf("Rebalanced: %+v\n", ntf)
		}
	}()

	datach := make(chan string)
	defer close(datach)
	go asyncSendDataProducer(datach)

	// consume messages, watch signals
	for {
		select {
		case msg, ok := <-consumer.Messages():
			if ok {
				datach <- string(msg.Value)
				//fmt.Fprintf(os.Stdout, "%s/%d/%d\t%s,\t%s,\t%s\n", msg.Topic, msg.Partition, msg.Offset, msg.Key, msg.Value,time.Now())
				consumer.MarkOffset(msg, "") // mark message as processed
			}
		case <-signals:
			return
		}
	}
}

func asyncSendDataProducer(data chan string) {
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true //必须有这个选项
	config.Producer.Timeout = 5 * time.Second
	//config.Producer.Compression = sarama.CompressionGZIP
	p, err := sarama.NewAsyncProducer(dataSendBrokers, config)
	defer p.Close()
	if err != nil {
		return
	}

	//必须有这个匿名函数内容
	go func(p sarama.AsyncProducer) {
		errors := p.Errors()
		success := p.Successes()
		for {
			select {
			case err := <-errors:
				if err != nil {
					glog.Errorln(err)
				}
			case <-success:
			}
		}
	}(p)

	var v string
	ok := true
	for ok {
		if v, ok = <-data; ok {
			var log interface{}
			var jsonMsg = []byte(v)
			errJson := jsoniter.ConfigCompatibleWithStandardLibrary.Unmarshal(jsonMsg, &log)
			if errJson != nil {
				fmt.Println("error:", errJson)
			}
			rsa := log.(map[string]interface{})

			messagestr := rsa["message"].(string)
			hostname := (rsa["beat"].(map[string]interface{}))["hostname"].(string)

			messArray := strings.Split(messagestr, "|")
			arrLength := len(messArray)
			if arrLength < 7 {
				fmt.Println("not invalid log :", v)
			} else {
				ip := messArray[5]
				mess := strings.Replace(messagestr, ip, ip+","+hostname, -1)

				//fmt.Fprintf(os.Stdout, "out: %+v,----------- %s,---------- %s\n", mess, hostname,ip)
				msg := &sarama.ProducerMessage{
					Topic: dataSendTopic,
					Value: sarama.ByteEncoder(mess),
				}
				p.Input() <- msg

				logTime, logTimeErr := strconv.ParseInt(messArray[1], 10, 64)
				if logTimeErr != nil {
					fmt.Println("time convert error . ", messArray[1])
				} else {
					t := time.Now()
					lastDiffTime = t.Unix()*1000 - logTime
					fmt.Println("diff time :", lastDiffTime)
				}
			}
		}
	}
}

func postWx(msg string) {
	client := &http.Client{}
	req, err := http.NewRequest("POST", "https://oapi.dingtalk.com/robot/send?access_token=1f5189ba8cd0626c3d8ead159d14d5e562e7c06b8710678cd0aa492bee1bf696", strings.NewReader(`{"msgtype": "text","text": {"content": "`+msg+`"},"at":{"atMobiles":["15311486182"]}}`))
	if err != nil {
		fmt.Println("occur an error")
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("occur an error")
	}
	fmt.Println(string(body))
}

func main() {
	c := cron.New()
	spec := "*/60 * * * * ?"
	c.AddFunc(spec, func() {
		if lastDiffTime > maxDiffTime {
			fmt.Println("start send wx message.", lastDiffTime)
			var timeStr string = string(time.Now().Format("2006-01-02 15:04:05"))
			postWx("时间：" + timeStr + ",日志转发有延时，延时时间：" + strconv.FormatInt((lastDiffTime/1000), 10) + "s")
		}
	})
	c.Start()
	consumer()
}
