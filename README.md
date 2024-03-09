# ICMT - 集成式代码管理工具

**集成式代码管理工具** (Integrated code management tools, **ICMT**) 使用云端存储，将代码保存于云端，可以避免代码丢失，而且方便管理，类似Git工具。

## 配置

- `config/global.json`中`site`键为ICMT服务端
- `config/user.json`中`user`键为用户信息，列表里有两项，分别为[username, password]注意使用英文逗号分隔

若为新用户，请先运行`signup`程序完成注册，再运行`main`

## 命令

### 项目有关

**项目需要在ICMT工具同文件夹下创建项目名文件夹！**

- `clone user/reponame`用于克隆他人项目，将他人项目代码存储到本地，`user`即用户名，`reponame`即用户的代码开源项目
- `new repo`创建项目，`repo`为项目名称。
- `merge`合并项目，即快速提交项目，将项目上传到云端，注意上传内容包括文件删减
- `ls user/reponame`查看某个项目的结构
- `delrepo reponame`删除项目

### 文件有关

ICMT区分了*项目操作*和*文件操作*，对单个文件的操作命令如下：

- `upload filename`上传名为`filename`的文件（可以为二进制）（考虑到上传大文件，上传大于1MB文件时生成分割的小文件属正常现象，上传完均会自动删除）
- `pull user/filename`拉取名为`filename`的文件（可以为二进制）并保存到本地
- `del filename`删除文件

### 其他

- `exit`，退出

## 开源

Apache 2.0 License