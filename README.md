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

# Запуск



