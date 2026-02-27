# -*- coding: utf-8 -*-

import re, time, datetime
import os, sys
from GestionBD import *

import csv
import datetime
import sys

import csv
import datetime
import sys

import csv
import datetime
import sys


def Crea_RetailersList(retailersList_csv):
    """
    Generates a CSV of retailers by duplicating each store for ALL modes present in table 'mode_commande'.

    Tables used:
    - Table modes : mode_commande (id_mdc, lib_mdc)
    - Table stores : master_data_mag (columns below)

    - VenueId = mag_code * 100 + id_mdc (assumes id_mdc < 100 ; see note below)
    """

    # DB Connection
    bd_GPM = GestionBD(Glob.dbName_GPM, Glob.user_GPM, Glob.passwd_GPM, Glob.host_GPM, Glob.port_GPM)

    if bd_GPM.echec:
        sys.exit(1)

    print("Start retrieving venueId : %s" % datetime.datetime.now())

    # 1) Dynamically retrieve all modes (zero hardcode)

    req_modes = "SELECT id_mdc, lib_mdc FROM mode_commande ORDER BY id_mdc"

    if not bd_GPM.executerReq(req_modes):
        print("QUERY EXECUTION ERROR (modes) : \n%s" % req_modes)

        try:
            bd_GPM.close()
        except:
            pass

        sys.exit(1)

    modes_rows = bd_GPM.resultatReq()

    if not modes_rows:
        print("No command mode found in 'mode_commande'.")

        try:
            bd_GPM.close()
        except:
            pass

        sys.exit(1)

    # List of id_mdc (int)

    try:
        modes = [int(r[0]) for r in modes_rows if r and r[0] is not None]

    except Exception:

        # Some drivers return Decimal → force int
        modes = [int(r[0]) for r in modes_rows if r and r[0] is not None]

    max_mode = max(modes)

    if max_mode >= 100:

        # Do not stop execution, but warn about collision risk

        print("WARNING : id_mdc max = %d >= 100 ; formula VenueId = mag_code*100 + id_mdc can cause collisions." % max_mode)

    print("Modes detected (%d) : %s" % (len(modes), modes))

    # 2) Retrieve stores (Shop/Channel columns come from master_data_mag)

    req_mags = """
    SELECT

        mag_code AS MagId,
        usi_code AS UsiId,
        usi_longname AS VenueLabel,
        mag_type AS UsiType,

        COALESCE(mag_surface, 0) AS SquareFootage,

        shop_code AS ShopCode,
        shop_shortname AS ShopLabel,
        shop_type AS ShopType,

        civ_cd_circ_vente AS ChannelId,
        civ_lb_circ_vente AS ChannelLabel

    FROM master_data_mag

    ORDER BY mag_code
    """

    if not bd_GPM.executerReq(req_mags):

        print("QUERY EXECUTION ERROR (stores) : \n%s" % req_mags)

        try:
            bd_GPM.close()
        except:
            pass

        sys.exit(1)

    mags = bd_GPM.resultatReq()

    nb_mags = len(mags)

    print("%d stores to process - %d modes - %d expected rows"
          % (nb_mags, len(modes), nb_mags * len(modes)))

    # 3) CSV Writing

    nb = 0

    f = None

    try:

        f = open(retailersList_csv, "w", newline='', buffering=1024 * 1024)

        writer = csv.writer(f,
                            delimiter=';',
                            lineterminator='\n',
                            quoting=csv.QUOTE_MINIMAL)

        writer.writerow([

            "VenueId",
            "MagId",
            "UsiId",
            "VenueLabel",
            "UsiType",
            "ShopCode",
            "ShopLabel",
            "ShopType",
            "ChannelId",
            "ChannelLabel",
            "SquareFootage"
        ])

        # Loop: duplicate each store for all modes

        for mag in mags:

            mag_id, usi_id, venue_lbl, usi_type, sqft, shop_code, shop_label, shop_type, channel_id, channel_lbl = mag

            # Normalize None → default values

            venue_lbl = "" if venue_lbl is None else venue_lbl
            usi_type = "" if usi_type is None else usi_type
            shop_label = "" if shop_label is None else shop_label
            shop_type = "" if shop_type is None else shop_type
            channel_lbl = "" if channel_lbl is None else channel_lbl
            sqft = 0 if sqft is None else sqft

            for mode_id in modes:

                venue_id = mag_id * 100 + mode_id

                row = [

                    venue_id,
                    mag_id,
                    usi_id,
                    venue_lbl,
                    usi_type,
                    shop_code,
                    shop_label,
                    shop_type,
                    channel_id,
                    channel_lbl,
                    sqft

                ]

                writer.writerow(row)

                nb += 1

    finally:

        try:
            if f:
                f.close()
        except:
            pass

        try:
            bd_GPM.close()
        except:
            pass

    print("%d venueId generated - %s"
          % (nb, datetime.datetime.now()))

    return 0


def Verif_RetailersList(retailersList_csv):

    # Create DB interface object

    bd_GPM = GestionBD(Glob.dbName_GPM,
                       Glob.user_GPM,
                       Glob.passwd_GPM,
                       Glob.host_GPM,
                       Glob.port_GPM)

    if bd_GPM.echec:
        sys.exit(1)

    print("Start verification export : "
          + str(datetime.datetime.now()))

    fic_exp = open(retailersList_csv, 'r')

    cdmag = 0

    ls_mag = []

    nb = 1

    for l in fic_exp:

        if nb > 1:

            cdmag = int(re.split(";", l)[1])

            if cdmag not in ls_mag:

                ls_mag.append(cdmag)

        nb += 1

    fic_exp.close()

    print("%d mag_code retrieved in file"
          % len(ls_mag))

    req_verif = """
    select
    mag_code,
    usi_code,
    mag_dt_debut,
    mag_dt_fin,
    mag_surface,
    shop_code,
    shop_shortname
    from master_data_mag
    """

    if bd_GPM.executerReq(req_verif):

        fic = open(retailersList_csv.replace(".csv", "_verif.csv"), "w")

        fic.writelines("mag_code;usi_code;mag_dt_debut;mag_dt_fin;mag_surface;shop_code;shop_shortname\n")

        res_mag = bd_GPM.resultatReq()

        for mag in res_mag:

            mag_code = mag[0]

            if mag_code not in ls_mag:

                fic.writelines("%s\n" % str(mag))

        fic.close()

    else:

        bd_GPM.close()

        print("QUERY EXECUTION ERROR : \n%s" % req_verif)

        return 1

    nbDiff = len(res_mag) - len(ls_mag)

    print("%d different mag_code retrieved"
          % nbDiff)

    return nbDiff


path = sys.argv[1]

RC = Crea_RetailersList(path + Glob.retailersList_csv)

if RC == 0:

    print("RetailersList creation finished. Verification running...")

    nbDiff = Verif_RetailersList(path + Glob.retailersList_csv)

    if nbDiff == 0:

        print("All stores present. OK")

        sys.exit(0)

    else:

        print("WARNING %d differences found" % nbDiff)

        sys.exit(1)

else:

    print("ERROR creating retailers list")

    sys.exit(1)