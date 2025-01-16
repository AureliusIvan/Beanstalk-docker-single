# regex for extracting data from the text
patterns = {
    "tnb": {
        "no_akaun": r"No\. Akaun\s*:\s*(\d+)",
        "no_kontrak": r"No\. Kontrak\s*:\s*(\d+)",
        "no_invois": r"No\. Invois\s*:\s*(\d+)",
        "jumlah_perlu_dibayar": r"Jumlah Perlu Dibayar\s*:\s*RM\s*([\d,]+\.\d{2})",
        "tarikh_bil": r"Tarikh Bil\s*:\s*(\d{2}\.\d{2}\.\d{4})",
        "tunggakan": r"Tunggakan\s*RM\s*([\d,]+\.\d{2})",
        "caj_semasa": r"Caj Semasa\s*RM\s*([\d,]+\.\d{2})",
        "bil_terdahulu": r"Bil Terdahulu\s*RM\s*([\d,]+\.\d{2})",
        "bayaran_akhir": r"Bayaran Akhir\s*RM\s*([\d,]+\.\d{2})",
        # "tarikh_bayaran_akhir": r"\(\d{2}\.\d{2}\.\d{4}\)"
    },
    "malakoff": {

    },
    "saj": {

    },
    "se": {

    },
    "laku_bintulu": {

    },
    "kuching": {

    },
    "iwk": {

    }
}
