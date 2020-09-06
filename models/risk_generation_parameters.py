class RiskGenerationParameters(object):
    def __init__(self, spatialDomain=None, temporalDomain=None, closeInSpace=None, closeInTime=None, caseThreshold=None, startDate=None, endDate=None, sridOfExtent=None, extentMinX=None, extentMinY=None, extentMaxX=None, extentMaxY=None, validate_parameters: bool = False):
        self.spatialDomain = spatialDomain
        self.temporalDomain = temporalDomain
        self.closeInSpace = closeInSpace
        self.closeInTime = closeInTime
        self.caseThreshold = caseThreshold
        self.startDate = startDate
        self.endDate = endDate
        self.sridOfExtent = sridOfExtent
        self.extentMinX = extentMinX
        self.extentMinY = extentMinY
        self.extentMaxX = extentMaxX
        self.extentMaxY = extentMaxY
        self.validate_parameters = validate_parameters

    @property
    def spatialDomain(self):
        return self._spatialDomain

    @spatialDomain.setter
    def spatialDomain(self, value):
        self.validate_not_empty(value, "Spatial Domain")
        self._spatialDomain = value

    @property
    def temporalDomain(self):
        return self._temporalDomain

    @temporalDomain.setter
    def temporalDomain(self, value):
        self.validate_not_empty(value, "Temporal Domain")
        self._temporalDomain = value

    @property
    def closeInSpace(self):
        return self._closeInSpace

    @closeInSpace.setter
    def closeInSpace(self, value):
        self.validate_not_empty(value, "Close In Space")
        self._closeInSpace = value

    @property
    def closeInTime(self):
        return self._closeInTime

    @closeInTime.setter
    def closeInTime(self, value):
        self.validate_not_empty(value, "Close In Time")
        self._closeInTime = value

    @property
    def caseThreshold(self):
        return self._caseThreshold

    @caseThreshold.setter
    def caseThreshold(self, value):
        self.validate_not_empty(value, "Case Threshold")
        self._caseThreshold = value

    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, value):
        self.validate_not_empty(value, "Start Date")
        self._startDate = value

    @property
    def endDate(self):
        return self._endDate

    @endDate.setter
    def endDate(self, value):
        self.validate_not_empty(value, "End Date")
        self._endDate = value

    @property
    def sridOfExtent(self):
        return self._sridOfExtent

    @sridOfExtent.setter
    def sridOfExtent(self, value):
        self.validate_not_empty(value, "SRID of Extent")
        self._sridOfExtent = value

    @property
    def extentMinX(self):
        return self._extentMinX

    @extentMinX.setter
    def extentMinX(self, value):
        self.validate_not_empty(value, "Extent Min X")
        self._extentMinX = value

    @property
    def extentMinY(self):
        return self._extentMinY

    @extentMinY.setter
    def extentMinY(self, value):
        self.validate_not_empty(value, "Extent Min Y")
        self._extentMinY = value

    @property
    def extentMaxX(self):
        return self._extentMaxX

    @extentMaxX.setter
    def extentMaxX(self, value):
        self.validate_not_empty(value, "Extent Max X")
        self._extentMaxX = value

    @property
    def extentMaxY(self):
        return self._extentMaxY

    @extentMaxY.setter
    def extentMaxY(self, value):
        self.validate_not_empty(value, "Extent Max Y")
        self._extentMaxY = value

    def validate_not_empty(self, value, property_name):
        if self.validate_parameters and not value:
            raise ValueError("{property_name} cannot be empty".format(property_name=property_name))
