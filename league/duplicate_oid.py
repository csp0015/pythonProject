class DuplicateOid(Exception):
    def __init__(self, oid):
        super().__init__(f"Duplicate OID: {oid}")
        self.oid = oid