import time
from MainframeExtractor.Helpers.EmulatorHelper import EmulatorHelper
from MainframeExtractor.Helpers.EmulatorHelper import EmulatorPosition
from Utils.StringUtils import StringUtils


class DBStarProPresum:
    def __init__(self, emulator):
        self.emulator = emulator

    def execute(self):
        # Select PRO-PRESUM
        EmulatorHelper.set_value(self.emulator, "PRO-PRESUM", EmulatorPosition(24, 32))
        time.sleep(1)  # sleeps because the connection may fail in between processes
        EmulatorHelper.go_to_next_screen(self.emulator)


class DBStarProPresumPTFM(DBStarProPresum):

    def run(self, ref_date, number_of_months):
        self.execute()

        # MENU GERAL DOS RESUMOS
        EmulatorHelper.set_value(self.emulator, "A", EmulatorPosition(20, 28))  # Opcao de Pesquisa: "Pesquisa Individual por Tipo"
        EmulatorHelper.set_value(self.emulator, "M", EmulatorPosition(21, 17))  # Periodicidade: "Mensal"
        EmulatorHelper.go_to_next_screen(self.emulator)

        # PESQUISA INDIVIDUAL POR TIPO (MENSAL)
        EmulatorHelper.set_value(self.emulator, "PTFM", EmulatorPosition(22, 37))  # Tipo de Resumo: "PTFM"
        EmulatorHelper.go_to_next_screen(self.emulator)

        self.extract_vol_data(ref_date, number_of_months)

    def set_ptfm_parameters(self, ref_date):
        EmulatorHelper.set_value(self.emulator, ref_date, EmulatorPosition(4, 49))  # Data de Referencia (MMAA)
        EmulatorHelper.set_value(self.emulator, "Q", EmulatorPosition(9, 49))  # Baumuster: "Q" - mostra todas variantes
        EmulatorHelper.set_value(self.emulator, "", EmulatorPosition(12, 49))  # Agrupamento de Produto - por denominacao: "" - vazio
        EmulatorHelper.set_value(self.emulator, "", EmulatorPosition(16, 49))  # Apresentacao: "Cliente/Baumuster"

    def extract_vol_data(self, ref_date, number_of_months):
        iterations = int(number_of_months / 12)  # calculate the number of iterations,
        if (number_of_months % 12) > 0:
            iterations += 1  # rectify to one up if not multiple of 12

        step_ref_date = ref_date
        for step in range(1, iterations):

            if step > 1:
                step_ref_date = self.get_next_ref_date(step_ref_date)

            self.set_ptfm_parameters(step_ref_date)
            EmulatorHelper.go_to_next_screen(self.emulator)

            step_number_of_months = 12
            if step == iterations:
                cu = number_of_months % 12
                if cu > 0:
                    step_number_of_months = cu

            self.xablau(step_number_of_months)

    def xablau(self, number_of_months):
        dates_header_list = self.emulator.string_get(6, 1, 80).strip().split(' ')
        dates_header_list = [item for item in dates_header_list if item != '']  # clean up empty data for consistency
        dates_header_list = dates_header_list[:number_of_months]  # resize to target size

        first_item = None
        current_item = self.get_current_item()
        next_item = None
        same_item = False

        while current_item != first_item:
            if first_item is None:
                first_item = current_item

            for volume_info in range(7, 18, 2):
                location_line = self.emulator.string_get(volume_info, 1, 80).strip()
                volume_line = self.emulator.string_get(volume_info+1, 1, 80).strip()

                if location_line != "" and volume_line != "":

                    register_info = location_line[0:25].strip().split('-')
                    cerep_info = location_line[25:80].strip().split('-')
                    volume_data_list = volume_line.split(' ')

                    register_code = register_info[0]
                    register_name = register_info[1]
                    cerep_code = cerep_info[0]
                    cerep_name = cerep_info[1]
                    volume_by_month = dict(zip(dates_header_list, volume_data_list))

            variant_id = StringUtils.remove_whitespace(current_item[1:29])
            variant_description = current_item[29:58].strip()

            # go to next item
            self.emulator.move_to(24, 80)
            self.emulator.send_enter()
            self.emulator.wait_for_field()
            next_item = self.get_current_item()

            if next_item == current_item:
                same_item = True
            else:
                same_item = False

    def get_current_item(self):
        item_pos = EmulatorPosition(4, 1)
        return EmulatorHelper.get_value(self.emulator, item_pos, 80)

    @staticmethod
    def get_next_ref_date(ref_date):
        month = ref_date[:2]
        next_year = int(ref_date[-2:]) + 1
        return month + str(next_year)
