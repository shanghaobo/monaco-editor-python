# monaco-editor-python

> monaco-editor 编辑器使用 jsonrpc-ws-proxy 和 python-language-server，实现 python 代码提示功能

## 效果

![](demo.gif)

## 运行步骤

#### 运行环境

- node.js 和 python 环境

#### 准备工作

- node.js 安装 npm 和 yarn
- python 安装`python-language-server`

  ```
  pip install 'python-language-server[all]'
  ```

#### 启动前端项目

- 进入 web 目录，依次运行以下命令启动前端项目

  ```
  yarn
  yarn prepare
  yarn run start
  ```

#### 启动语言代理

- 方式一：Python 代理（推荐）

  进入`server2`目录，运行以下命令启动代理程序

  ```
  python examples/langserver_ext.py
  ```

  Github 仓库：[https://github.com/shanghaobo/python-jsonrpc-server](https://github.com/shanghaobo/python-jsonrpc-server)

- 方式二：node.js 代理

  进入 `server`目录，依次运行以下命令启动代理程序

  ```
  npm install
  npm run prepare
  node dist/server.js --port 5000 --languageServers servers.yml
  ```

5. 访问 `http://localhost:3000`

## 博客教程

[https://www.qinyu.cc/archives/137.html](https://www.qinyu.cc/archives/137.html)
