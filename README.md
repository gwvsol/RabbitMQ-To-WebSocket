## RabbitMQ-To-WebSocket    
---   

Сервис для передачи данных из очереди RabbitMQ в Websocket    

Использование   
```shell
make fastapiws	- Installing the project
make uninstall	- Deleting a project
make build	 - Building services in Docker
make start	 - Running services in Docker
make stop	 - Stopping services in Docker
make restart - Restart services in Docker
make log	 - Displaying service logs in Docker
make remove	 - Deleting services in Docker
```    

Все необходимые настройки задаются в ```.env```

Подписываемся на WebSocket с использованием [```websocat```](https://github.com/vi/websocat)   

```websocat ws://192.168.10.14:9015/ws```