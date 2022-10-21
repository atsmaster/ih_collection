class CareInfo:

    def __init__(self):
        self.__url = ''
        self.__care_nm = ''
        self.__care_nm_en = ''
        # self.__page = ''

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, val):
        self.__url = val

    @property
    def care_nm(self):
        return self.__care_nm

    @care_nm.setter
    def care_nm(self, val):
        self.__care_nm = val

    @property
    def care_nm_en(self):
        return self.__care_nm_en

    @care_nm_en.setter
    def care_nm_en(self, val):
        self.__care_nm_en = val

    # @property
    # def page(self):
    #     return self.__page
    #
    # @page.setter
    # def page(self, val):
    #     self.__page = val
