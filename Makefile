deploy:
	@eb init --region us-east-1 --keyname "aws-eb" --tags "Name=TestBeanStalk" --profile default --platform python-3.12
	# for available platforms, run `eb platform list`
	@eb create TestBeanStalk --single --platform python-3.12 --enable-spot -v
	@eb deploy TestBeanStalk --verbose --debug
	@eb open


terminate:
	@eb terminate TestBeanStalk --force
	@eb delete TestBeanStalk --force
	@eb terminate --all --force
	@eb delete --all --force
	@eb cleanup --force
	@eb labs cleanup-versions


build:
	@docker build -t beanstalkdocker .

run:
	@docker run -p 8000:8000 beanstalkdocker