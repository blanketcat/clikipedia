# mysql dockerfile

FROM ubuntu:16.04

RUN apt-get update && apt-get -y upgrade

# set the variables to take care of install menu options
RUN export DEBIAN_FRONTEND="noninteractive"
RUN sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password rootpw"
RUN sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password rootpw"

RUN sudo apt-get install -y mysql-server-5.7

RUN mysql_secure_installation

