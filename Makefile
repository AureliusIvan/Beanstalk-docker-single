deploy:
	@eb init --region us-east-1 --keyname "aws-eb" --tags "Name=BeanstalkDocker" --profile default --platform docker
	# for available platforms, run `eb platform list`
	@eb create BeanstalkDocker --single --platform docker --enable-spot -v
	@eb deploy BeanstalkDocker --verbose --debug
	@eb open


terminate:
	@eb terminate BeanstalkDocker --force
	@eb delete BeanstalkDocker --force
	@eb terminate --all --force
	@eb delete --all --force
	@eb cleanup --force
	@eb labs cleanup-versions


build:
	docker build -t beanstalkdocker .

run:
	docker run --rm -p 8000:8000 --name beanstalkdocker-container beanstalkdocker


auth:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 058264163083.dkr.ecr.us-east-1.amazonaws.com

push:
	docker tag beanstalkdocker:latest 058264163083.dkr.ecr.us-east-1.amazonaws.com/python/backendrepo:latest
	docker push 058264163083.dkr.ecr.us-east-1.amazonaws.com/python/backendrepo:latest