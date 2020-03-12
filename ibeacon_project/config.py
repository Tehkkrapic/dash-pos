DRINK_IDS = {
 "espresso" : 2.01,
 "kratka_kava" : 2.02,
 "kakao_s_mlijekom" : 3.01,
 "duga_kava_espresso": 2.03,
 "duga_kava_nescafe" : 2.04,
 "irish_kava" : 3.02,
 "cokolada" : 3.03,
 "macchiato_espresso" : 3.04,
 "macchiato_nescafe" : 3.05,
 "irish_macchiato" : 3.06,
 "pojacana_cokolada" : 3.07,
 "cappuccino" : 3.08,
 "cappuccino_nescafe" : 3.09,
 "irish_cappuccino" : 3.10,
 "cokolada_s_mlijekom" : 3.11,
 "capp_s_cok_esp" : 3.12,
 "capp_s_cok_nes": 3.13,
 "irish_cap_s_coko" : 3.14,
 "mocaccino_espresso" : 3.15,
 "mocaccino_nescafe" : 3.16,
 "mocaccino_irish" : 3.17,
 "caj" : 2.05
}

DRINK_UUIDS = {
 "caj" : "5e05fefc-5e14-4352-ad28-ece7a569dde8",
 "cappuccino" : "561a1bfc-3eaf-4cfa-83f1-cfbceaab2f17"
}

MACHINE_ID = '<YOUR-MACHINE-ID>'
MACHINE_API_KEY = 'Api-Key <YOUR-API-KEY>'
MACHINE_API_URL = '<YOUR-API-IP>/vending/purchases/create/'

# set this to the full path to the dash-pos respository checkout
DASHVEND_DIR = '/home/pi/dash-pos'
# note: also update paths in:
#   bin/conversion/conversion_dash_hrk.py

DASHD_PATH = '<YOUR-PATH-TO-DASHD-DIR>'
DASHCORE_DIR = '<YOUR-PATH-TO-DASHCORE-DIR>'
# after testing, set this to True to use mainnet
MAINNET = True
