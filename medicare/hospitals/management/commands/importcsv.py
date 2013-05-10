from csv import DictReader
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from medicare.hospitals import models


class Command(BaseCommand):
    """
    Import a CSV file of data. Provide a path to the file.
    """
    args = '<path path ...>'
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

    def __init__(self, *args, **kwargs):
        self.help = self.__doc__
        self.hospital_fieldnames = self.fieldnames[1:8]
        self.procedure_fieldnames = self.fieldnames[8:]
        super(Command, self).__init__(*args, **kwargs)

    def get_hospital(self, row):
        hospital = dict([(f, row[f]) for f in self.hospital_fieldnames])
        return hospital["id"], hospital

    def get_procedure(self, row):
        procedure_id, name = row["procedure"].split(" - ", 1)
        return procedure_id, {"id": procedure_id, "name": name}

    def get_hospital_procedure(self, row):
        procedure_id, _ = self.get_procedure(row)
        procedure = dict([(f, row[f]) for f in self.procedure_fieldnames])
        procedure["hospital_id"] = row["id"]
        procedure["procedure_id"] = procedure_id
        return procedure

    def get_rows(self, csv_path):
        if not path.exists(csv_path):
            raise CommandError("The file {0} does not exist or could not be read.".format(csv_path))
        with open("../Medicare_Provider_Charge_Inpatient_2011.csv") as fh:
            for row in DictReader(fh, self.fieldnames):
                    # Exclude the header row.
                    if row["id"].isdigit():
                        yield row

    def handle(self, csv_path, *args, **options):
        hospitals = {}
        procedures = {}
        hospital_procedures = []
        for row in self.get_rows(csv_path):
            hospital_key, hospital = self.get_hospital(row)
            if hospital_key not in hospitals:
                hospitals[hospital_key] = hospital
            procedure_key, procedure = self.get_procedure(row)
            if procedure_key not in procedures:
                procedures[procedure_key] = procedure
            hospital_procedures.append(self.get_hospital_procedure(row))
        with transaction.commit_on_success():
            cursor = connection.cursor()

            cursor.execute("DELETE FROM hospitals_hospital")
            transaction.commit_unless_managed()
            models.Hospital.objects.bulk_create([models.Hospital(**h) for h in hospitals.values()])

            cursor.execute("DELETE FROM hospitals_procedure")
            transaction.commit_unless_managed()
            models.Procedure.objects.bulk_create([models.Procedure(**p) for p in procedures.values()])

            cursor.execute("DELETE FROM hospitals_hospitalprocedure")
            transaction.commit_unless_managed()
            models.HospitalProcedure.objects.bulk_create([models.HospitalProcedure(**hp) for hp in hospital_procedures])
