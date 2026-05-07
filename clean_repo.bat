@echo off
REM === Настройки ===
set REPO_URL=https://github.com/jkonstantin1028-max/audiobook_movie_bot.git
set BFG_PATH=C:\tools\bfg\bfg-1.15.0.jar

REM === Клонируем зеркало ===
git clone --mirror %REPO_URL%
cd audiobook_movie_bot.git

REM === Удаляем медиафайлы через BFG ===
java -jar "%BFG_PATH%" --delete-folders books --delete-folders movies --delete-files *.mp3 --delete-files *.mp4

REM === Чистим историю ===
git reflog expire --expire=now --all
git gc --prune=now --aggressive --force

REM === Форс-пуш обратно на GitHub ===
git push origin --force

echo ==========================================
echo Репозиторий очищен и отправлен на GitHub!
echo ==========================================
pause
