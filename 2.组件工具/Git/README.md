# Git 工具的学习

## git bash 显示中文和解决乱码

- git status 不显示中文问题
  - 症状：在默认设置下，中文文件名在工作区状态输出，中文名不能正确显示，而是显示为八进制的字符编码。
  - 解决：
  - > git config --global core.quotepath false
  - ![截图](./assets/7DE3E1EA-9746-4475-BF52-FC1ECB867277.png)

- git 中文乱码问题
  - 修改gitconfig配置文件
    - 编辑etc\gitconfig文件，也有些windows系统是存放在C:\Users\Administrator\.gitconfig路径或安装盘符:\Git\mingw64\etc\gitconfig，在文件末尾增加以下内容

```bash
[gui]  
encoding = utf-8  
# 代码库统一使用utf-8  
[i18n]  
    commitencoding = utf-8  
    # log编码  
[svn]  
    pathnameencoding = utf-8  
    # 支持中文路径  
[core]
    quotepath = false
    # status引用路径不再是八进制（反过来说就是允许显示中文了）
```

### git submodule git的子项目管理  

> 有时需要建立一个父项目，来统一管理各个子项目，进行版本兼容性测试，统一发布，统一编排等等。

```bash
git submodule add/status/init/deinit/summary/foreach/sync/

# 添加子模块：
git submodule add URL

# 带有submodule的项目进行本地clone。
git clone URL --recursive

# 更新子模块：
git submodule init/update
git submodule update --init --recursive


# 获取子模块更新：
git submodule foreach git pull

# 删除子模块：
git rm --cached MODULENAME
git -rf MODULENAME
vim .git/config  # 中删除相关的submodule中的MODULENAME信息

```

## git fork后跟踪原始repo的方法

> 有时自己需要fork别人的项目来进行一些定制化开发。一段时间后别人的项目也进行了bug修复和新功能开发，这时就需要跟踪并且合并到自己项目中。

```bash
git remote 命令添加多个远程仓库，然后进行远程仓库的本地化合并。

# 查看远程仓库
git remote -v

# 添加远程仓库URL
git remote add upstreamName URL

# 更新远程仓库信息到本地。
git fetch upstreamName

# 合并远程仓库内容到本地分支。
git checkout master  # 回到想要合并的分支。
git merge upstreamName/master  # 合并更新内容。

# 如果本地仓库和upstreamName仓库是自己fork，并且独立管理的，会出现报错：
# Error: Git refusing to merge unrelated histories
git merge upstreamName/master --allow-unrelated-histories
```

## git 管理分支

### 使用到的shell脚本

```shell
# 判断分支是否存在
exists_branch_tag() {
    for arg in "$@"
    do
    res=$(git branch |grep -w "$arg" || git tag -l |grep -w "$arg")
    if [ $? -ne 0 ]; then
    echo -e "分支:$arg 不存在"
    return 1
    fi
    done
    echo -e "#@"
    return 0
}

# 判断tag是否存在
exists_tag() {
    for arg in "$@"
    do
        res=$(git tag -l|grep -w "$arg")
        if [[  $? -eq 0 ]] && [[ ${#arg} -eq 20 ]] && [[ "${arg:0:1}" -eq "b" || "${arg:0:1}" -eq "r" ]]; then
            :
        else
            echo -e "Tag :$arg 不存在"
            return 1
        fi
    done
    echo -e "$@"
    return 0
}

# 获取最后提交的commitid
branch_last_commitid() {
    if [ $# -ge 1 ]; then
        # 参数未分支名称
        echo -e $(git log -n 1 --pretty=format:"%h" "$1")
    else
        echo -e $(git log -n 1 --pretty=format:"%h")
    fi
}

# 比较B 是否在A 之后提交了新内容
diff_log_two_branchs() {
    first_branch=$1
    [ $# -lt 2 ] && second_branch='master' || second_branch=$2

    res=$(exists_branch_tag $first_branch $second_branch)
    [  $? -ne 0 ] && echo -e "$res" && return 1

    foward_branch=$(git log $first_branch..$second_branch)
    if [ -z "$foward_branch" ];then
        echo -e "分支先后顺序正常"
        return 0
    else
        echo -e "分支:{$second_branch}有新提交,请先合并到$first_branch上:\n $foward_branch"
        return 1
    fi
}

# 生成btag
create_btag() {
    commitId=$(branch_last_commitid)
    btime=$(date +"%y%m%d%H%M")
    btag="b-$btime-${commitId}"
    # 当前代码 恢复commit,然后打btag
    res=$(git reset "${commitId}" --hard && git tag "$btag" && git push origin "$btag")
    [  $? -ne 0 ] && echo -e "$res" && return 1
    # delete remote tag
    # git push origin :refs/tags/"$btag"
    echo -e "$btag"
    return 0
}

# 把A 合并到 B 上
merge_push() {
    first_branch=$1
    [[ $# -lt 2 ]] && second_branch='master' || second_branch=$2

    res=$(exists_branch_tag $first_branch $second_branch)
    [[ $? -ne 0 ]] && echo -e $res && return 1

    # 判断second_branch是否有新的独立提交
    res=$(diff_log_two_branchs $first_branch $second_branch)
    [[ $? -ne 0 ]] && echo -e $res && return 1

    # 代码回归到最后分支,强制更新代码
    git reset HEAD --hard && git checkout $first_branch && git pull origin $first_branch || git pull origin refs/tags/$first_branch
    # 合并到master上。
    git checkout $second_branch && git pull origin $second_branch || git pull origin refs/tags/$second_branch
    merge_res=$(git merge --no-ff $first_branch|grep -wE "CONFLICT \(content\)|Automatic merge failed")
    if [ $? -eq 0 ]; then
        #有冲突
        git reset HEAD --hard
        echo -e "在$second_branch 上合并$first_branch 有冲突,请修复后重试:\n $merge_res"
        return 1
    fi
    git push origin "$second_branch"
    echo -e "merge $first_branch 到 $second_branch 成功"
    return 0
}

# rtag 合并
# 将rtag A 合并到 B 上
create_rtag() {
    first_branch=$1
    [[ $# -lt 2 ]] && second_branch='master' || second_branch=$2

    # 判断 A 是否是btag
    res=$(exists_tag $first_branch)
    [[ $? -ne 0 ]] && echo -e $res && return 1

    # 进行合并
    res=$(merge_push $first_branch $second_branch)
    [[ $? -ne 0 ]] && echo -e $res && return 1

    # 打rtag, 选择A的最后一个commitid目的是rtag和btag有联系
    commitId=$(branch_last_commitid $first_branch)
    rtime=$(date +"%y%m%d%H%M")
    rtag="r-$rtime-${commitId}"
    git checkout $second_branch
    git tag "$rtag"
    git push origin "$rtag"
    echo -e "$rtag"
    return 0
}
```

### 分支处理

```shell
# 清理当前分支，并check到新的分支或者tag上。
git reset HEAD --hard && git checkout $branch && git pull origin $branch || git pull origin refs/tags/$branch
```