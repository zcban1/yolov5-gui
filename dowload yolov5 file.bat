@echo off
setlocal

:: Clona il repository YOLOv5 nella cartella corrente
git clone https://github.com/ultralytics/yolov5.git

:: Verifica se il clone è stato eseguito con successo
if %errorlevel% neq 0 (
    echo Errore durante il clone del repository YOLOv5.
) else (
    echo YOLOv5 è stato scaricato con successo nella cartella corrente.

    :: Sposta nella cartella YOLOv5
    cd "yolov5"

    :: Aggiorna alla versione più recente
    git pull

    :: Verifica se l'aggiornamento è stato eseguito con successo
    if %errorlevel% neq 0 (
        echo Errore durante l'aggiornamento di YOLOv5.
    ) else (
        echo YOLOv5 è stato aggiornato con successo all'ultima versione.
    )
)

endlocal

