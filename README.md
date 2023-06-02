# Описание проекта

Проект представляет FRONTEND и API для проекта YaMDb.
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся.
По адресу http://127.0.0.1:8000/redoc/ к нему подключена документация.

# Способы реализации проекта:

Проект реализован на фреймворке Django.

Примененение вьюсетов.

# Пользовательские роли и права доступа

Аноним — может просматривать описания произведений, читать отзывы и комментарии.

Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

Аутентифицированным пользователям разрешено оставлять к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Добавлять произведения, категории и жанры может только администратор.

# Установка

## 1) Склонировать репозиторий
`git@github.com:Yandexpract/api_yamdb.git`

## 2) Создать виртуальное окружение для проекта
`python -m venv venv`


## 3) Активировать виртуальное окружение для проекта
`. venv/Scripts/activate`

## 4) Установить зависимости
`pip install -r requirements.txt`

## 5) Выполнить миграции
`python manage.py makemigrations`
`python manage.py migrate`

## 5) Запустить сервер
`python manage.py runserver`

# Примеры

Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт
 'api/v1/users/' (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения. 
После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт '/api/v1/auth/signup/' , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на заппрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.
