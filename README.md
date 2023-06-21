# PDF Summarizer

## Running with Docker
```shell
docker build -t pdf .
docker run -p 8080:8080 -v PATH_TO_UPLOADS:/app/uploads pdf
```

## Running without Docker
```shell
cd src
python app.py
```