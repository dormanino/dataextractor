from BPM_STAR_Extractors.Models.QVVPartialVolumeData import QVVPartialVolumeData


class QVVPartialSalesData:

    def __init__(self, data, order_location_name, order_location_number_cerep,
                 register_name, register_number, total_volume):
        self.data = data
        self.order_location_name = order_location_name
        self.order_location_number_cerep = order_location_number_cerep
        self.register_name = register_name
        self.register_number = register_number
        self.total_volume = int(total_volume)

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            list(map(QVVPartialVolumeData.from_dict, datadict[QVVPartialSalesData.JSONKeys.data])),
            datadict[QVVPartialSalesData.JSONKeys.order_location_name],
            datadict[QVVPartialSalesData.JSONKeys.order_location_number_cerep],
            datadict[QVVPartialSalesData.JSONKeys.register_name],
            datadict[QVVPartialSalesData.JSONKeys.register_number],
            datadict[QVVPartialSalesData.JSONKeys.total_volume]
        )

    class JSONKeys:
        data = "data"
        order_location_name = "order_location_name"
        order_location_number_cerep = "order_location_number_cerep"
        register_name = "register_name"
        register_number = "register_number"
        total_volume = "total_volume"
