# 这是一个用来快速发布 Django + REST API 的镜像，基于 python3.7.1
# 项目的发布仅仅使用了 uginx，所以如果Django项目中需要处理静态文件，请使用Nginx
# 该镜像只支持 MySQL 数据库
FROM python:3.7.1
MAINTAINER junebao<15364968962@163.com>
ENV PROJECT_PATH /usr/local/django
ENV PROJECT_NAME project
RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*
# pip配置阿里云
RUN mkdir ~/.pip
RUN touch ~/.pip/pip.conf
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf
RUN echo "[install]" >> ~/.pip/pip.conf
RUN echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf
RUN pip install --upgrade pip
RUN pip install django==2.2.7
RUN pip install djangorestframework==3.9.4
RUN pip install mysqlclient
RUN pip install pytz==2019.1
RUN pip install sqlparse==0.3.0
RUN pip install django-cors-headers==3.2.0 
RUN pip install uwsgi
WORKDIR $PROJECT_PATH
RUN cd $PROJECT_PATH
# 生成一个project的django project
RUN django-admin startproject project
RUN mkdir $PROJECT_PATH/logs && touch $PROJECT_PATH/logs/uwsgi.log
# 建立uwsgi.ini文件
RUN touch $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
# TODO：往ini文件中写入相关配置
RUN echo "# junebao/DRMI uwsgi.ini" > $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo "[uwsgi]" >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo "http = :8000" >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo chdir = $PROJECT_PATH/$PROJECT_NAME >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo module = $PROJECT_NAME.wsgi >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo logto = $PROJECT_PATH/logs/uwsgi.log >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo "master = true" >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo "processes = 4" >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
RUN echo "vacuum = true" >> $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini
EXPOSE 8000
CMD /usr/local/bin/uwsgi --ini $PROJECT_PATH/$PROJECT_NAME/uwsgi.ini