## Загрузка фотографий космоса в Telegram

Скрипт для постинга фотографий космоса в Telegram.  
Фотографии загружаются с сервисов NASA и SpaceX.  
Постинг осуществляется с помощью Telegram бота.  

### Как пользоваться
Вам понадобятся:  
API-ключ NASA (получить можно здесь https://api.nasa.gov/).  
Токен Telegram бота (подробнее о ботах можно почитать здесь https://core.telegram.org/bots).  
id канала в Telegram куда будет происходить постинг.  

Положите файл .env в корень папки со скриптом и укажите в нём следующие переменные окружения:  
    
    NASA_TOKEN="{Ваш API-ключ NASA}"
    TELEGRAM_TOKEN="{Токен вашего Telegram бота}"
    TG_CHAT_ID="{id канала для постинга фото}"
    SCRIPT_DELAY=86400

Скрипт публикует фотографии раз в сутки. Изменить интервал вы можете с помощью переменной окружения "SCRIPT_DELAY". 
Интервал указывается в секундах.  

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

    pip install -r requirements.txt

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.