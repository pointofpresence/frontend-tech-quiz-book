# Пример из кода на Dependency Injection

### Категории

Dependency injection, Design patterns, Technical, Software architecture

### Краткий ответ

**Пример из кода на Dependency Injection**

- Dependency Injection (DI) — паттерн для управления зависимостями
- Инверсия управления: объекты получают зависимости извне
- Обеспечивает **слабую связанность** и удобство тестирования
- Пример на Python:

```python
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self, engine):
        self.engine = engine  # DI через конструктор

    def drive(self):
        self.engine.start()
        print("Car is driving")

engine = Engine()
car = Car(engine)
car.drive()
```

- DI позволяет подставить другой `Engine` для тестов или альтернатив

- В больших проектах DI-фреймворки (Spring, Guice, Dagger) автоматизируют внедрение зависимостей

- Важно: зависимости передаются, а не создаются внутри класса — ключ DI

Этот пример демонстрирует принцип DI: класс `Car` не создаёт `Engine`, а получает его извне. Это повышает гибкость и упрощает тестирование кода.

### Подробный ответ
#### Основной ответ
**Dependency Injection (DI)** — это паттерн проектирования, при котором зависимости объекта (например, сервисы, репозитории) передаются ему извне, а не создаются внутри самого объекта. Это повышает тестируемость, гибкость и поддерживаемость кода, разделяя ответственность за создание зависимостей и их использование.

#### Ключевые моменты
- В классическом примере на **C# с .NET Core** зависимости обычно передаются через конструктор (Constructor Injection). Это самый популярный и понятный способ DI.
- DI-контейнер (например, встроенный в ASP.NET Core) управляет временем жизни объектов и разрешает зависимости автоматически.
- Такой подход уменьшает жёсткую связанность компонетов и упрощает замену реализации для моков или альтернатив в тестах.

#### Пример кода (C#)

```csharp
public interface ILogger
{
    void Log(string message);
}

public class ConsoleLogger : ILogger
{
    public void Log(string message) => Console.WriteLine(message);
}

public class UserService
{
    private readonly ILogger _logger;

    // Dependency Injection через конструктор
    public UserService(ILogger logger)
    {
        _logger = logger;
    }

    public void CreateUser(string username)
    {
        // Логируем создание пользователя
        _logger.Log($"User '{username}' created.");
    }
}

// Регистрация и использование
var serviceProvider = new ServiceCollection()
    .AddSingleton<ILogger, ConsoleLogger>()
    .AddTransient<UserService>()
    .BuildServiceProvider();

var userService = serviceProvider.GetService<UserService>();
userService.CreateUser("Ivan");
```

#### Практический контекст
В реальном проекте DI помогает управлять сложной иерархией зависимостей — например, сервисы доступа к данным, логирования, кэширования, внешних API. Благодаря DI легче писать модульные тесты, заменяя конкретные реализации на мок-объекты. В ASP.NET Core версии 3.1+ и выше встроенный DI-контейнер — стандарт для управления зависимостями.
