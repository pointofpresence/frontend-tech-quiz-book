# Приведи пример зависимости/регистрации с Zenject

**Пример зависимости/регистрации с Zenject**  
- Zenject — DI фреймворк для Unity  
- регистрация через Container (например, Container.Bind<T>())  
- зависит от интерфейса или класса (Bind<IService>().To<Service>().AsSingle())  
- внедрение через конструктор, поля, свойства  
- пример:  
```csharp
public interface IService { }  
public class Service : IService { }  

public class Installer : MonoInstaller 
{
    public override void InstallBindings()
    {
        Container.Bind<IService>().To<Service>().AsSingle();
    }
}
```
- в классе-потребителе:
```csharp
public class Consumer
{
    private readonly IService _service;
    public Consumer(IService service) { _service = service; }
}
```
- Zenject автоматически создаст Service и внедрит в Consumer  
- упрощает тестирование и управление зависимостями в Unity проектах

# Подробный ответ
## Основной ответ
**Zenject** — это мощный dependency injection (DI) framework для Unity, позволяющий удобно управлять зависимостями в проекте. Пример простой регистрации и разрешения зависимости через Zenject — это регистрация интерфейса и внедрение его в класс, который нуждается в этой функциональности.

```csharp
// Интерфейс зависимости
public interface IWeapon 
{
    void Shoot();
}

// Конкретная реализация
public class Pistol : IWeapon 
{
    public void Shoot() { Debug.Log("Pistol shooting"); }
}

// Класс, куда внедряется зависимость
public class Player 
{
    private IWeapon _weapon;

    // Конструктор с [Inject] для обозначения зависимостей
    [Inject]
    public Player(IWeapon weapon) 
    { 
        _weapon = weapon; 
    }

    public void Attack() 
    {
        _weapon.Shoot();
    }
}

// В классе Installer, где происходит регистрация
public class GameInstaller : MonoInstaller 
{
    public override void InstallBindings() 
    {
        Container.Bind<IWeapon>().To<Pistol>().AsSingle();
        Container.Bind<Player>().AsSingle();
    }
}
```

## Ключевые моменты
- **Container.Bind<Interface>().To<Implementation>().AsSingle()** — стандартный паттерн для регистрации зависимости с синглтон-жизненным циклом.
- Внедрение через конструктор с **[Inject]**, что является рекомендуемым способом для тестируемого и чистого кода.
- Zenject позволяет гибко управлять временем жизни (Singleton, Transient и др.), что критично для сложных игровых сценариев.

## Практический контекст
В реальных проектах Zenject часто используется для декомпозиции логики в Unity: например, разные системы игры (оружие, инвентарь, AI) регистрируются в контейнере, и объект игрока получает нужные зависимости без жёсткой связи. Это упрощает модульное тестирование, замену реализаций (например, смену оружия на другой класс) и масштабирование кода.
