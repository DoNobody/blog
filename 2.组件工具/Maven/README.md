# Maven的学习日常

## 常见问题解决

- 出现Generating project in Interactive mode 等待问题

> -DarchetypeCatalog=internal

## VScode 中maven项目支持

> 默认VScode 中支持的插件Java Extension Pack, 对java项目的支持都是需要eclipse风格的项目
> 即: 需要 `.project`, `classpath` 两个文件
> 可以通过执行 `mvn eclipse:eclipse` 命令进行项目转换，即可生成上述两个文件。
> 然后通过vscode的`JAVA DEPENDENCIES` 插件查看依赖的包
