# 使用官方的Python 3.8映像作为基础映像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有内容到容器的工作目录
COPY . /app

# 安装Flask和其他必要的依赖项
RUN pip install -r requirements.txt

# 暴露容器的端口
EXPOSE 5000

# 启动应用程序
CMD ["python", "app.py"]
