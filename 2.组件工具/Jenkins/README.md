# jenkins

## 项目持续集成调度器

```bash
pipeline {
    agent any
    parameters {
        string(name: 'JOB_DATE', defaultValue: '', description: '任务日期yyyyMMdd')
    }
    stages {
        stage('Parallel Stage') {
            failFast false
            parallel {
                stage('Branch A') {
                    agent {
                        label "Marmot-dnode02"
                    }
                    steps {
                        aaa= {build job: 'Marmot-1-m2h-ods-jianlc-interest', parameters: [string(name: 'JOB_DATE', value: "${JOB_DATE}")],wait:true}
                        echo aaa.number
                    }
                }
                stage('Branch B') {
                    agent {
                        label "Marmot-dnode02"
                    }
                    steps {
                        bbb={build job: 'Marmot-1-m2h-ods-product', parameters: [string(name: 'JOB_DATE',value: "${JOB_DATE}")],wait:true}
                        echo bbb.result
                    }
                }
            }
        }
    }
}
```

## 一段可以并行运行的pipeline脚本

```java
// 定义一个任务的构建函数，调用方需要等待任务完成
def generateStage(item) {
    return {
        stage("${item}") {
            build job: "${item}", parameters: [string(name: 'JOB_DATE', value: "${JOB_DATE}")],wait:true
        }
    }
}

// 定义并行任务的名称列表
def ODS_NAMES = ['/ODS_JMZQ/Marmot-1-m2h-ods-stock_market','/ODS_JMZQ/Marmot-1-m2h-ods-stock_mgmt','/ODS_JMZQ/Marmot-1-m2h-ods-stock_news','/ODS_JMZQ/Marmot-1-m2h-ods-stock_trade','/ODS_JMZQ/Marmot-1-m2h-ods-stock_user']

// 定义一个并行任务的列表
def OdsParallelStagesMap = ODS_NAMES.collectEntries {
    ["${it}" : generateStage(it)]
}

def ETLS_NAMES=[]

def EtlsParallelStagesMap = ETLS_NAMES.collectEntries {
    ["${it}" : generateStage(it)]
}

def H2MS_NAMES=[]

def H2msParallelStagesMap = H2MS_NAMES.collectEntries {
    ["${it}" : generateStage(it)]
}

def FIX_H2MS_NAMES=[]

def Fixh2msParallelStagesMap = FIX_H2MS_NAMES.collectEntries {
    ["${it}" : generateStage(it)]
}

pipeline {
    agent any
    parameters {
        string(name: 'JOB_DATE', defaultValue: '', description: '任务日期yyyyMMdd')
    }
    triggers {
        cron('10 0 * * *')
    }
    stages {
        stage('Marmot-1-m2h-ods') {
            agent {
                label "Marmot-dnode01"
            }
            steps {
                script {
                    // parallel 并行化执行
                    parallel OdsParallelStagesMap
                }
            }
        }
        stage('xstrom_ops01_etls') {
            agent {
                label "ops01"
            }
            steps {
                script {
                    parallel EtlsParallelStagesMap
                }
            }
        }
        stage('xstrom_ops01_h2ms') {
            agent {
                label "ops01"
            }
            steps {
                script {
                    parallel H2msParallelStagesMap
                }
            }
        }
        stage('Marmot-2-h2h-facts-build') {
            agent {
                label "Marmot-dnode02"
            }
            steps {
                // 直接调用其他任务
                build job: "Marmot-2-h2h-facts-build", parameters: [string(name: 'JOB_DATE', value: "${JOB_DATE}")],wait:true
            }
        }
    }
    post {
        failure {
            dingTalk accessToken: 'xxx', imageUrl: '', jenkinsUrl: '', message: '', notifyPeople: ''
        }
        success {
            dingTalk accessToken: 'xxxx', imageUrl: '', jenkinsUrl: '', message: '', notifyPeople: ''
        }
        aborted {
            dingTalk accessToken: 'xxxx', imageUrl: '', jenkinsUrl: '', message: '', notifyPeople: ''
        }
    }
}
```
