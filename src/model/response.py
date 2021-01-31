from src.model.exception import *


class Response:
    """
    All responses have in common that they have a status

    """

    def __init__(self, status):
        self.status = status

    def validate(self):
        """
        Validate the status

        Throws ValueError that is catched when calling this, don't worry
        :return:
        """

        if self.status and self.status == "error":
            raise ValueError("Error in response status")
        elif self.status and self.status == "success":
            return True
        raise ValueError("Response status does not have a valid value!")


class ApiResponse(Response):
    """
    Represents a simple api response

    """

    def __init__(self, status, message):
        self.message = message
        super().__init__(status)

    def validate(self):
        """
        Validate

        Throws: ApiConnectionError, ValidationError
        :return: True if is valid, or exception if not
        """

        # Check status of response
        try:
            super().validate()
        except ValueError as err:
            raise ApiResponseError(ApiResponse(self.status, self.message))

        # Validate
        if self.message and type(self.message) == str:
            return True
        elif self.message and not type(self.message) == str:
            raise ValidationError("Message is not of type string!")
        elif not self.message:
            raise ValidationError("Message is None!")
        else:
            raise ValidationError("The scary else that should never happen")


class FolderCreateResponse(Response):
    pass


class AccountInfoResponse(Response):
    pass


class ServicesListResponse(Response):
    pass


class CacheCheckResponse(Response):
    pass


class ZipGenerateResponse(Response):
    pass


class TransferListResponse(Response):
    pass


class TransferDirectDlResponse(Response):
    pass


class TransferCreateResponse(Response):
    pass


class ItemDetailsResponse(Response):
    pass


class FolderSearchResponse(Response):
    pass


class FolderListResponse(Response):
    pass

