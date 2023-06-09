## Expo

Для мобильной версии будем использовать фреймворк Expo
(он просто работает поверх React Native)

Просто запуск приложения:
```
npm run start
```
Далее он спросит, под какую платформу запустить

Запуск под конкретную платформу:
```
npm run android
// или
npm run web
```

Изменения в коде появляются в реальном времени

---

## Запуск под Android

Понадобится установить [Android Studio](https://developer.android.com/studio). 
Запустить его и [установить SDK](https://maxfad.ru/programmer/android/83-ustanovka-android-studio-nastrojka-sdk.html)

Если подключен обычный телефон, то запускаться будет на нем автоматически.
Надо будет только включить [режим разработчика](https://smartphonus.com/как-включить-режим-разработчика-на-android/)

В Android Studio можно создать [эмулятор](https://developer.android.com/studio/run/managing-avds), чтобы не подключать телефон. 
Если телефон не подключен, то запускаться будет сразу на эмуляторе.
Эмулятор запустится сам. После создания эмулятора в Android Studio можно больше не заходить.

Можно запустить просто в браузере, включив через F12 экран смартфона.
Тогда запускаем ```npm run web```

---

## Feature sliced design

[Туториал на YouTube](https://youtu.be/c3JGBdxfYcU?t=1620)

Короче, у нас есть:
1. Слои
2. Слайсы внутри слоев (модули с index.ts)
3. Сегменты внутри слайсов

### Слои:
Каждый слой использует только нижележащие. 
На своем слое также ничего использовать нельзя.


1. app
   - настройки, глобальные стили, провайдеры
   - в React Native __не используется CSS__ - все стили хранятся в объектах. Поэтому мы будем хранить глобальные стили в shared
2. processes
   - опциональный слой
   - сценарии между страницами (аутентификая и пр.)
3. pages
   - страницы. Объединяют в себе widgets и features
4. widgets
   - самостоятельные блоки
5. features 
   - есть бизнес-ценность
   - пользовательские сценарии
6. entities
   - бизнес-модели и все относящееся
   - например, форма связанная с User
7. shared
   - функциональность без привязки к проекту
   - UI-Kit
   - __тут слайсов нет, сразу идут сегменты__

Я добавил циферки к названиям слоев, чтобы они располагались по порядку в WebStorm

### Слайс (модули)

Папка (модуль) с файлом index.ts, внутри которого находятся сегменты.
У каждого модуля - свой отдельный слайс в Redux

### Сегменты:

Это следующие папки:

- UI / components 
- model (Redux: store, actions, модели и пр.)
- lib (utils, hooks)
- config (опционально)
- api
- consts

### Слой App:


