from csv import DictReader
from decimal import Decimal
from re import compile

fieldnames = (
    "procedure",
    "id",
    "name",
    "address",
    "city",
    "state",
    "zipcode",
    "region",
    "discharges",
    "avg_covered_charges",
    "avg_total_payments",
)

hospial_fieldnames = fieldnames[2:8]
procedure_fieldnames = fieldnames[8:]
procedure_id = compile("^(\d+)")


def is_not_header_row(row):
    """
    Hospital IDs are alwyas numeric.
    """
    return row["id"].isdigit()


def process_procedure(row):
    """
    Split a string into a procedure ID and name.
    """
    #proc_id, proc_name = row["procedure"].split(" - ", 1)
    procedure = dict([(f, row[f]) for f in procedure_fieldnames])
    procedure["avg_covered_charges"] = Decimal(procedure["avg_covered_charges"])
    procedure["avg_total_payments"] = Decimal(procedure["avg_total_payments"])
    return row["procedure"], procedure


hospitals = {}

with open("../Medicare_Provider_Charge_Inpatient_2011.csv") as fh:
    for row in DictReader(fh, fieldnames):
        if is_not_header_row(row):
            if row["id"] not in hospitals:
                hospitals[row["id"]] = dict([(f, row[f]) for f in hospial_fieldnames])
                hospitals[row["id"]]["procedures"] = {}

            proc_id, procedure = process_procedure(row)
            hospitals[row["id"]]["procedures"][proc_id] = procedure






