
class INodeLayout:

    def DoLayout(self, bounds, graph, **kwargs):
        raise NotImplementedError("@DoLayout: must be implemented");
