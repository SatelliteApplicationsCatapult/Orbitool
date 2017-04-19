from collections import defaultdict
import numpy as np

def datatable_to_dict(table, job_id, db):
    """
    Reads dicts of numpy arrays from database
    args:
        table e.g dbLinkBudget.SAT
        job_id eg 1
        db eg. dbLinkBudget
    output is a dictionary of np arrays
    """
    keys = list(table.fields)
    keys.remove("Job_ID")
    keys.remove("id")
    mydict = defaultdict(list)
    row_list=db(table.Job_ID == job_id).iterselect(*keys).as_list()
    for row in range(0,len(row_list)):
        for key, value in row_list[row]['_extra'].items():
            mydict[key] = np.append(mydict[key],value)
    return mydict


def write_dict_to_table(table, dic, job_id, db):
    # type: (object, object, object) -> object
    """
    Used to read in dictionaries which contain
    np arrays created when reading from database

    Args:
        table: db table eg db.SAT
        dic: dictionary of arrays
        job_id: is the scenario ID

    """
    row = dic.fromkeys(dic)
    for v in range(dic.values()[0].size):
        for k in range(len(dic.keys())):
            row[dic.keys()[k]] = dic.values()[k][v]
        job_id_check = table.Job_ID == job_id
        if table is db.Gateway:
            table.update_or_insert((table.GW_ID == row['GW_ID']) & (job_id_check), Job_ID=job_id,
                                **row) #all these query if these fields are equal. If so then updates. Otherwise inserts
        elif table is db.SAT:
            table.update_or_insert((table.SAT_ID == row['SAT_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif table is db.TRSP:
            table.update_or_insert((table.TRSP_ID == row['TRSP_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif table is db.VSAT:
            table.update_or_insert((table.VSAT_ID == row['VSAT_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif table is db.Earth_coord_GW:
            table.update_or_insert(
                (job_id_check) & (table.LON == row['LON']) & (table.LAT == row['LAT']) & (table.GW_ID == row['GW_ID']) & (
                    table.TRSP_ID == row['TRSP_ID']), Job_ID=job_id, **row)
        elif table is db.EARTH_coord_VSAT:
            table.update_or_insert((job_id_check) & (table.LON == row['LON']) & (table.LAT == row['LAT']) & (table.VSAT_ID == row['VSAT_ID']), Job_ID=job_id, **row)

        else:
            table.update_or_insert(Job_ID=job_id, **row)
