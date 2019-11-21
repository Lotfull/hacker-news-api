# appfollow-hacker-news
Приложение, которое периодически парсит главную страницу Hacker News, вытягивая из нее список постов и сохраняя в базу данных.
Приложение имеет HTTP API с одним методом (GET /posts), с помощью которого можно получить список всех доступных (собранных) новостей.
По каждой новости имеется заголовок и URL, а также время, когда она была сохранена в БД. Сохраняется только 30 новостей. Новые загружаются через определенный интервал времени, либо по-требованию.

API метод для получения списка новостей на запрос: 
    
    curl -X GET http://localhost:8000/posts

Результат список новостей в формате JSON
    
    [
      {"id": 1, "title": "Announcing Rust 1.33.0", "url": "https://example.com", "created": "ISO 8601"},
      {"id": 2, "title": "Redesigning GitHub Repository Page", "url": "https://example.com", "created": "ISO 8601"}
    ]

Работать сортировка по заданному атрибуту, по возрастанию и убыванию.
    
    curl -X GET http://localhost:8000/posts?order=title

Имеется возможность запросить подмножество данных, указав offset и limit. По-умолчанию API возвращает 5 постов.
    
    curl -X GET http://localhost:8000/posts?offset=10&limit=10

Гитхаб репозиторий: https://github.com/Lotfull/appfollow-hacker-news
Приложение доступно по ссылке: appfollow.lotfullin.com
Используется Docker
Код покрыт тестами pytest

# Launch

## Settings
Настройки API могут быть изменены в файле `.env`

Запуск Django в режиме DEBUG=True если MODE=LOCAL, иначе DEBUG=False:
   
    MODE=LOCAL

Установка ограничения на количество постов в базе данных (по умолчанию без ограничения):
   
    #POSTS_DB_LIMIT=30

Параметр limit по умолчанию:
   
    POSTS_API_LIMIT_DEFAULT=5

Максимальное значение параметра limit:
   
    POSTS_API_LIMIT_MAX=100

Имя хоста для удалённого запуска:
   
    HOST_IP=localhost


## Local

    pip3 install -r requirements.txt
    cp -n .env_example .env
    python3 manage.py migrate
    python3 -u manage.py runserver
    
## Docker

    docker-compose up