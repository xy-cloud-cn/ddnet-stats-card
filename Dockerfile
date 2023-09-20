FROM python:3.10
# 配置工作目录
WORKDIR /DDNStatsCard

# 拷贝当前目录所有的文件，进入 docker 镜像中
COPY . .

# 执行安装 Python 环境依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露 80 端口，给外部使用，因为上面我们开启的是 80 端口
EXPOSE 8080

# 使用 gunicorn 运行 Flask 项目，最后一个命令： app:app  前者对应的是flask 启动 文件，后面不要乱改
CMD gunicorn -c gunicorn.conf index:app
