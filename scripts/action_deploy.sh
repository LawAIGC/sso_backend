SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
echo "PROJECT_DIR: $PROJECT_DIR"

git restore .
git switch main
git pull

docker-compose down

docker-compose up --build -d

sleep 10

docker-compose ps
