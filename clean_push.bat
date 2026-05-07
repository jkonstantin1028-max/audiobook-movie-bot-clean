@echo off
cd /d E:\Rabota\audiobook-movie-bot

echo === Удаляем старую .git ===
rmdir /s /q .git

echo === Инициализация нового репозитория ===
git init
git checkout -b main
git remote add origin https://github.com/jkonstantin1028-max/audiobook-movie-bot.git

echo === Добавляем файлы и коммитим ===
git add .
git commit -m "Clean commit after BFG cleanup"

echo === Форс-пуш на GitHub ===
git push --set-upstream origin main --force

echo === Готово! Проверь репозиторий на GitHub ===
pause
