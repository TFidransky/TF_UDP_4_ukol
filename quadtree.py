import uuid

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class QuadTree:
    def __init__(self, NL_point, NR_point, SL_point, SR_point, result):
        self.result = result
        self.features = []
        self.NL_point = NL_point
        self.SR_point = SR_point
        self.NR_point = NR_point
        self.SL_point = SL_point
        self.NL_child = None
        self.NR_child = None
        self.SR_child = None
        self.SL_child = None

    def divide(self):
        if len(self.features) <= 50:
            id = uuid.uuid1().__str__()
            for feature in self.features:
                self.result.append(self.setFeatureGroup(feature, id))

            return

        mid = Point((self.NL_point.x + self.SR_point.x)/2, (self.NL_point.y + self.SR_point.y)/2)

        for feature in self.features:
            if feature.x_coord <= mid.x and feature.y_coord >= mid.y:
                if(self.NL_child == None):
                    self.NL_child = QuadTree(self.NL_point, Point(mid.x, self.NL_point.y), Point(self.NL_point.x, mid.y), Point(mid.x, mid.y), self.result)
                self.NL_child.insert(feature)
            elif feature.x_coord >= mid.x and feature.y_coord >= mid.y:
                if (self.NR_child == None):
                    self.NR_child = QuadTree(Point(mid.x, self.NR_point.y), self.NR_point, Point(mid.x, mid.y), Point(self.NR_point.x, mid.y), self.result)
                self.NR_child.insert(feature)
            elif feature.x_coord >= mid.x and feature.y_coord <= mid.y:
                if (self.SR_child == None):
                    self.SR_child = QuadTree(Point(mid.x, mid.y), Point(self.NR_point.x, mid.y), Point(mid.x, self.SL_point.y), self.SR_point, self.result)
                self.SR_child.insert(feature)
            else:
                if (self.SL_child == None):
                    self.SL_child = QuadTree(Point(self.NL_point.x, mid.y), Point(mid.x, mid.y), self.SL_point, Point(mid.x, self.SL_point.y), self.result)
                self.SL_child.insert(feature)

        if(self.NL_child != None):
            self.NL_child.divide()
        if (self.NR_child != None):
            self.NR_child.divide()
        if (self.SL_child != None):
            self.SL_child.divide()
        if (self.SR_child != None):
            self.SR_child.divide()

    def insert(self, feature):
        self.features.append(feature)

    def setFeatureGroup(self, feature, id):
        feature.feature["cluster_id"] = id
        return feature