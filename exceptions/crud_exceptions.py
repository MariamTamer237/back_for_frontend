from fastapi import HTTPException, status


class BasicHTTPException(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code=status_code, detail=detail)


class EntityNotFoundError(HTTPException):
    def __init__(self, entity_type, entity_id=None, id_type="ID"):
        if entity_id:
            self.message = f"{entity_type} with {id_type} {entity_id} not found"
        else:
            self.message = f"{entity_type} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": self.message}
        )


class EntityAlreadyExistsError(HTTPException):
    def __init__(self, entity_type, entity_id=None, id_type="ID"):
        if entity_id:
            self.message = f"A {entity_type} with {id_type} {entity_id} already exists."
        else:
            self.message = f"{entity_type} already exists."

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": self.message}
        )


class EntityParentNotFoundError(HTTPException):
    def __init__(self, entity_type, entity_id, parent_id):
        self.message = (
            f"{entity_type} with ID {entity_id} has parent ID {parent_id} not found."
        )
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": self.message}
        )