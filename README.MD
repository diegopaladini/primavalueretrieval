Prima Value Retrieval

## Setup e avvio
1. Installare la distribuzione di Python 3 adatta alla versione di Windows https://www.python.org/ftp/python/3.8.8/python-3.8.8-amd64.exe
2. Alla fine dell'installazione di python spuntare l'opzione 'ADD TO %PATH%'
3. Unzip cartella dello script sulla cartella dell'utente ad esempio 'anni'
4. Salvare la cartella dei log con il nome 'data' in minuscolo e posizionarla nella stessa cartella dello script
5. Aprire il promnt comandi (finestra nera con le scritte) 
6. Digitare il seguente comando (installazione dei comandi in gergo 'dipendenze')
   ```
   pip install -r requirements.txt
   ```
7. Digitare il seguente comando per avviare lo script
   ```
   python primavalueretrieval.py -i input_dir -o output_dir
   ```
