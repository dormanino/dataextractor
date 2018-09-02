import json
import datetime
from BPM_STAR_Extractors.DataPoint import DataPoint
from BPM_STAR_Extractors.String_Parser import Parse
import time


class Xyz:

    @staticmethod
    def load_12mpp_raw():
        return json.load(open(DataPoint.data_12mpp))

    @staticmethod
    def load_b3902v_raw():
        return json.load(open(DataPoint.data_variant_final_data))

    @staticmethod
    def load_12mpp_parsed():
        return json.load(open(DataPoint.data_12mpp_parsed))

    @staticmethod
    def load_qvvs_with_volume():
        return json.load(open(DataPoint.data_qvv_bm_vol))

    @staticmethod
    def load_family_bu_info():
        return json.load(open(DataPoint.data_info_bm))

    @staticmethod
    def load_main_gen_file():
        return json.load(open(DataPoint.data_final_dict))

    @staticmethod
    def string_divide(string, div):
        l = []
        strp = ''
        i = 0
        while i < len(string):
            strp = string[i:i + div].strip().replace(" ", "")
            if strp != '':
                if Xyz.is_float_try(strp):
                    strp = int(strp)
                l.append(strp)
            i += div
        return l

    @staticmethod
    def is_float_try(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def zyx():
        return Xyz.load_b3902v_raw()


class MakeFile:

    @staticmethod
    def parsed_12mpp():
        # generates file xxxxxx12mpp_parsed based on xxxxxx12mpp.json('raw')
        x = Xyz.load_12mpp_raw()
        nd = {}
        lista = []
        month_list = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

        for key, val in x.items():
            for i in val[1]:
                lista = Parse.parse(i)
            # TODO: change json from list with one string to only string
            nd[key[slice(1, 29)].strip().replace(' ', '')] = dict(zip(month_list, lista))

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + "_12mpp_parsed.json", "w") as f:
            json.dump(nd, f, indent=4, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def bmqvvvol():
        b3902v = Xyz.zyx()
        dozempp = Xyz.load_12mpp_parsed()
        # TODO: dict comprehension
        dicto_tst = {}
        for b in b3902v:
            dicto_tst[str(b['variant'])] = b['baumuster'][0:7]

        final_dict = {}
        # TODO: dict comprehension
        for dc in dozempp:
            if dozempp[dc]['total'] != '0':
                final_dict[dc] = dozempp[dc]['total']

        for f in final_dict:
            for b in dicto_tst:
                if f == b:
                    volume = final_dict[f]
                    final_dict[f] = dicto_tst[b], volume
                    break

        set_bm = set()
        for dt in final_dict.values():
            set_bm.add(dt[0])
        print(set_bm)

        data_sum = 0
        dict_tst = {}
        data_tot_sum = 0
        for po in set_bm:
            for dt in final_dict.items():
                if po == dt[1][0]:
                    data_sum += int(dt[1][1])
            data_tot_sum += data_sum
            dict_tst[po] = data_sum
            data_sum = 0

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_qvv_bmvol.json', 'w') as f:
            json.dump(final_dict, f, indent=2, sort_keys=True, ensure_ascii=False)

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_bmvol_tot.json', 'w') as f:
            json.dump(dict_tst, f, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def concatenateinfos():
        qvv_info = Xyz.load_qvvs_with_volume()
        b3902v_info = Xyz.load_b3902v_raw()
        gen_info = Xyz.load_family_bu_info()
        prog_prod = Xyz.load_12mpp_parsed()

        dicto = {}
        qvv_with_volume_list = [[key, val] for key, val in qvv_info.items()]
        info_a_ver = [[info, bm] for info, bm in gen_info.items()]
        for bm_qvv in qvv_with_volume_list:
            for bm_info in info_a_ver:
                if bm_info[0] == bm_qvv[1][0]:
                    dicto[bm_qvv[0]] = bm_info
        for key_dicto, val_dicto in dicto.items():
            if key_dicto in prog_prod:
                dicto[key_dicto] = [dicto[key_dicto], prog_prod[key_dicto]]

        data_prev = {val['variant']: val['codes'] for val in b3902v_info}

        for key_dicto, val_dicto in dicto.items():
            if key_dicto in data_prev:
                dicto[key_dicto] = [dicto[key_dicto], data_prev[key_dicto]]

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_dict_end.json', 'w') as f:
            json.dump(dicto, f, indent=4, sort_keys=True, ensure_ascii=False)
    print('dict_end.json concluded')


MakeFile.parsed_12mpp()
MakeFile.bmqvvvol()
MakeFile.concatenateinfos()
