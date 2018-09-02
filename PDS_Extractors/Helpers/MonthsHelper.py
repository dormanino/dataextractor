from typing import Dict


class MonthsHelper:

    # Numeric representation of a month_year, pt-BR keys
    numeric: Dict[str, int] = dict(jan=1, fev=2, mar=3, abr=4, mai=5, jun=6,
                                   jul=7, ago=8, set=9, out=10, nov=11, dez=12,
                                   feb=2, apr=4, may=5, aug=8, sep=9, oct=10, dec=12)

    # English name of a month_year, pt-BR keys
    english: Dict[str, str] = dict(jan="jan",
                                   fev="feb",
                                   mar="mar",
                                   abr="apr",
                                   mai="may",
                                   jun="jun",
                                   jul="jul",
                                   ago="aug",
                                   set="sep",
                                   out="oct",
                                   nov="nov",
                                   dez="dec")
