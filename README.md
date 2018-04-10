# poop-iot

This project is inspired by the Twilio [blog post](https://www.twilio.com/blog/2018/03/iot-poop-button-python-twilio-aws.html).

It adds a couple of additions that were not in the original blog post

* KMS integration
* Rate limiting - Because toddlers like to click buttons

## Package for deployment

### Method 1
```bash
pip install -r requirements.txt -t .
zip -r poop-iot.zip *
```

### Method 2 - This requires having docker installed
```
pip insall make-lambda-package
make-lambda-package --requirements-file=requirements.txt .
```
