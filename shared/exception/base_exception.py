class BaseApiException(Exception):
    def __init__(self, code: str, message: str, stage: str, domain: str, target: str):
        super().__init__(message)
        self.code = code
        self.stage = stage
        self.domain = domain
        self.target = target
        self.response = { 
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "stage": stage,
                "domain": domain,
                "target": target
            }
        }