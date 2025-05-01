FROM gregoriotoscano/python311:latest 
LABEL AUTHOR="Gregorio Toscano <gtoscano@fastmail.com>"

# Environment Vars
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=utf8
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LC_CTYPE="en_US.UTF-8"
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/lib
ENV LD_RUN_PATH=/usr/local/lib:/usr/lib
ENV AMQP_USERNAME=guest
ENV AMQP_PASSWORD=guest
ENV SQL_DATABASE=mydb
ENV SQL_USER=myuser
ENV SQL_PASSWORD=32ghukj45ihhkj3425
ENV SQL_PORT=3306
ARG DOCKER_GID=994  # Default fallback

# fail the build if /version doesn’t exist
RUN if [ ! -f /version ]; then \
  echo "Error: /version not found" >&2; \
  exit 1; \
  fi

RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install apt-utils locales-all locales wget
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN mkdir -p /app/home /code





#WORKDIR /app/data/dependencies/
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y build-essential cmake \
  zip unzip \
  python3-pip python-is-python3 python3-psycopg2 \
  software-properties-common apt-transport-https \
  gnupg2 curl ca-certificates vim docker.io


# Install Node.js 20.x (example); adjust to your preference
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y nodejs

RUN groupmod -g ${DOCKER_GID} docker

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh
RUN pip install uuid sqlalchemy redis gunicorn watchdog
# https://github.com/ajaxorg/ace-builds.git
# Install pipenv
# If an error, use % pipenv lock
RUN pip install --upgrade pip && \
  pip install pipenv


EXPOSE 8080

WORKDIR /app/
COPY --chown=www-data:www-data . ./

# COPY . ./
RUN chown -R www-data:www-data /app && \
  chmod +x /app/docker-entrypoint.sh && \
  chown -R www-data:www-data /code

RUN pipenv install --system --deploy

RUN usermod -a -G docker www-data 
RUN usermod -d /app/home www-data 

USER www-data 

ENTRYPOINT ["/app/docker-entrypoint.sh"]

