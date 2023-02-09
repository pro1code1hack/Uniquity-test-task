class APIRequest:

    @classmethod
    def make_request(cls, aws_url: str, data: dict):
        import requests
        response = requests.post(aws_url, data=data)
        print(response)

        # TODO log response
