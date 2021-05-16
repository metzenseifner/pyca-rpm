all:
	docker-compose up

build:
	docker pull centos:8
	docker-compose build

rebuild:
	docker-compose up --build

clean:
	docker-compose down --volumes --remove-orphans
	rm -rf build/centos8/*

ci: rebuild
	@failed_containers=$$(docker-compose ps -q | xargs docker inspect -f '{{ .State.ExitCode }}' | grep -v '^0' | wc -l | tr -d ' '); \
	if [ "$$failed_containers" -ne 0 ]; then \
		echo "Build failures ocurred in $$failed_containers environments"; \
	  exit 1; \
	fi

.PHONY: all build rebuild clean ci
