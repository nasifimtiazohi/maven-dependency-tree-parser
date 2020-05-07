class depTreeNode():
    def __init__(self, group, artifact, version, packaging, scope=None, depth=None, parent=None):
        self.group=group
        self.artifact=artifact
        self.version=version
        self.packaging=packaging
        self.scope=scope
        self.depth=depth
        self.parent=parent
        self.children=None

